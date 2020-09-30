import os
import shutil
import json
import re
from collections import defaultdict

from .rdf_utils import get_rdf_uri
from .rdf_utils import get_fe_uris_and_labels

from .utils import remove_and_create_folder

from .res.FrameNetNLTK import generate_lu_rdf_uri


def lemma_from_lexemes(lexemes,
                       separator=' '):
    """
    given a list of dictionaries, each dictionary
    representing a lexeme,
    reconstruct the lemma

    :param list lexemes: list of dictionaries
    :param string separator: how to join
    the lexemes if 'breakBefore' = 'false'

    :rtype: str
    :return: the lemma
    """
    order_to_lexeme = {}

    for lexeme in lexemes:
        order = int(lexeme['order'])
        order_to_lexeme[order] = lexeme

    parts = []
    for order, lexeme in order_to_lexeme.items():
        if lexeme['breakBefore'] == 'true':
            part = lexeme['name'] + separator
        else:
            part = lexeme['name']

        parts.append(part)

    lemma = ''.join(parts)
    return lemma

def create_lexicon_data_annotation_tool(path_readme,
                                        path_ud_information,
                                        path_mapping_ud_pos_to_fn_pos,
                                        output_folder,
                                        verbose=0):
    """
    create a folder with FrameNet information to be used in the annotation tool

    :param str path_readme: path to read of the documents that it will contain, e.g.,
    documentation/lexicon_data_for_frame_annotation_tool/README.md
    :param str path_ud_information: JSON file mapping UD pos tag to more information about the label
    :param str path_mapping_ud_pos_to_fn_pos: JSON file mapping UD pos tag to FN pos tag
    :param str output_folder: where the folder should be stored, e.g., "lexicon_data_annotation_tool"
    """
    # recreate folder if needed
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    pos_folder = os.path.join(output_folder, 'part_of_speech')
    if not os.path.exists(pos_folder):
        os.mkdir(pos_folder)

    # write readme
    output_path_readme = os.path.join(output_folder, 'README.md')
    shutil.copy(path_readme, output_path_readme)

    if verbose:
        print(f'written README to {output_path_readme}')

    # write UD information
    output_path_ud_information = os.path.join(pos_folder, 'part_of_speech_ud_info.json')
    shutil.copy(path_ud_information, output_path_ud_information)

    if verbose:
        print(f'written UD information to {output_path_ud_information}')

    # write mapping UD pos to FN pos
    output_path_mapping_ud_fn = os.path.join(pos_folder, 'ud_pos_to_fn_pos.json')
    shutil.copy(path_mapping_ud_pos_to_fn_pos, output_path_mapping_ud_fn)

    if verbose:
        print(f'written mapping UD to FN to {output_path_mapping_ud_fn}')


def add_frame_to_info(output_folder,
                      fn_en,
                      premon,
                      verbose=0):
    """
    add the file frame_to_info.json to the folder with lexical data
    for the annotation tool

    :param str output_folder: output folder containing the lexical data for the annotation tool
    :param fn_en: english framenet in the nltk format
    """
    frame_rdf_uri_to_info = {}

    for frame in fn_en.frames():

        label = frame.name

        frame_rdf_uri = get_rdf_uri(premon_nt=premon,
                                    frame_label=label)

        fes = []
        label_to_fe_uri = get_fe_uris_and_labels(premon_nt=premon,
                                                 frame_uri=frame_rdf_uri)

        for fe_label, fe in frame.FE.items():
            fe_rdf_uri = label_to_fe_uri[fe_label]

            fe_info = {
                'definition': fe.definition,
                'rdf_uri': fe_rdf_uri,
                'fe_label': fe.name,
                'fe_type': fe.coreType
            }
            fes.append(fe_info)

        info = {
            'definition': frame.definition,
            'frame_label': frame.name,
            'framenet_url': frame.URL,
            'frame_elements': fes
        }

        frame_rdf_uri_to_info[frame_rdf_uri] = info

    if verbose:
        print()
        print(f'found {len(frame_rdf_uri_to_info)} frames')

    lexicons_folder = os.path.join(output_folder, 'lexicons')
    if not os.path.exists(lexicons_folder):
        os.mkdir(lexicons_folder)

    output_path_frame_to_info = os.path.join(lexicons_folder, 'frame_to_info.json')
    with open(output_path_frame_to_info, mode='w', encoding='utf8') as outfile:
        json.dump(frame_rdf_uri_to_info,
                  outfile,
                  indent=4,
                  ensure_ascii=False,
                  sort_keys=True)

    if verbose:
        print(f'written frame_to_info to {output_path_frame_to_info}')



def add_lu_to_info(your_fn,
                   language,
                   premon,
                   namespace,
                   major_version,
                   minor_version,
                   output_folder,
                   verbose=0):
    """
    Create one file at:
    LANGUAGE
        lu_to_info.json

    with the structure
    lu_url
        'frame_uri' : frame rdf uri of frame it evokes
        'lu_name' : the lu name
        'lu_id' : the lu identifier
        'lu_definition' : the lu definition
        'lexical_entries' : list of tuples (lemma, pos)

    :param your_fn: a FrameNet in NLTK format
    :param str language: nl (Dutch) and en (English) are supported
    :param str premon: PreMOn graph, load probably from res/premon/premon-2018a-fn17-noinf.nt
    :param str namespace: the namespace to use to generate lu_urls, e.g., http://rdf.cltl.nl/
    :param int major_version: major version of your framenet
    :param int minor_version: minor version of your framenet
    :param str output_folder: output folder containing the lexical data for the annotation tool
    :param str mw_separator: how to join multi-word expressions, e.g., with ' ' or '_'
    """
    assert language in {'en', 'nl'}, f'specified language ({language}) is not supported: nl | en'

    # remove and create dir if needed
    lexicons_folder = os.path.join(output_folder, 'lexicons')
    if not os.path.exists(lexicons_folder):
        os.mkdir(lexicons_folder)
    lang_dir = os.path.join(lexicons_folder, language)
    remove_and_create_folder(lang_dir)

    # create dict
    lu_to_info = {}

    for frame in your_fn.frames():

        label = frame.name

        frame_rdf_uri = get_rdf_uri(premon_nt=premon,
                                    frame_label=label)

        for lu_label, lu in frame.lexUnit.items():
            pos = lu.POS

            lu_url = generate_lu_rdf_uri(your_fn=your_fn,
                                         namespace=namespace,
                                         language=language,
                                         major_version=major_version,
                                         minor_version=minor_version,
                                         lu_id=lu.ID)

            # get lexical entries
            lexical_entries = set()

            main_lu_lemma, lu_pos = lu_label.rsplit('.', 1)
            all_lu_lemmas = lemmas_from_lu_name(lu_lemma=main_lu_lemma)

            for lu_lemma in all_lu_lemmas:
                lexical_entries.add((lu_lemma, pos))

            info = {
                'lu_id' : lu.ID,
                'lu_definition' : lu.definition,
                'lu_name' : lu_label,
                'lexical_entries' : list(lexical_entries),
                'frame_uri' : frame_rdf_uri,
                'frame_label' : label
            }

            lu_to_info[lu_url] = info

    if verbose:
        print(f'found info for {len(lu_to_info)} LUs')

    # save
    output_path = os.path.join(lang_dir, 'lu_to_info.json')
    with open(output_path, mode='w', encoding='utf-8') as outfile:
        json.dump(lu_to_info,
                  outfile,
                  indent=4,
                  ensure_ascii=False,
                  sort_keys=True)

    if verbose:
        print(f'written lu_to_info to {output_path}')


def add_lemma_to_pos_to_lu_urls(output_folder,
                                language,
                                verbose=0):
    """
    in the output folder, there exists:

    OUTPUT_FOLDER
        lexicons
            LANGUAGE
                lu_to_info.json

    this function will add lemma_to_pos_to_lus.json
    to the LANGUAGE folder

    :param str output_folder: output folder containing the lexical data for the annotation tool
    :param str language: nl (Dutch) and en (English) are supported
    """
    assert language in {'en', 'nl'}, f'specified language ({language}) is not supported: nl | en'

    lu_to_info_path = os.path.join(output_folder,
                                   'lexicons',
                                   language,
                                   'lu_to_info.json')

    error_message = f'{lu_to_info_path} does not exist, please first create lu_to_info.json'
    assert os.path.exists(lu_to_info_path), error_message

    lu_to_info = json.load(open(lu_to_info_path))


    lemma_to_pos_to_lus = {}

    for lu_url, lu_info in lu_to_info.items():
        for (lemma, pos) in lu_info['lexical_entries']:

            if lemma not in lemma_to_pos_to_lus:
                lemma_to_pos_to_lus[lemma] = defaultdict(list)

            if lu_url not in lemma_to_pos_to_lus[lemma][pos]:
                lemma_to_pos_to_lus[lemma][pos].append(lu_url)

    output_path = os.path.join(output_folder,
                               'lexicons',
                                language,
                                'lemma_to_pos_to_lus.json')

    with open(output_path, 'w') as outfile:
        json.dump(lemma_to_pos_to_lus,
                  outfile,
                  indent=4,
                  ensure_ascii=False,
                  sort_keys=True
                  )
    if verbose:
        print(f'written {output_path} to disk')
        print(f'{len(lemma_to_pos_to_lus)} lemmas contain a mapping to an LU.')




def lemmas_from_lu_name(lu_lemma):
    """

    :param str lu_lemma: the lu_name minus .POS, e.g., election for election.n

    :rtype: set
    :return: a set of lemmas
    """
    lemmas = set()

    table = {ord('(') : '',
             ord(')') : '',
             ord('[') : '',
             ord(']') : ''}

    if all(['[' in lu_lemma,
            ']' in lu_lemma]):
        # regex for ' [*]'
        lemma_without = re.sub(r" ?\[[^)]+\] ?", " ", lu_lemma)
        lemma_without = lemma_without.strip()

        lemma_with = lu_lemma.translate(table)
        lemmas.update([lemma_without, lemma_with])

    elif all(['(' in lu_lemma,
              ')' in lu_lemma]):
        # and with and without
        lemma_without = re.sub(r" ?\([^)]+\) ?", " ", lu_lemma)
        lemma_without = lemma_without.strip()

        lemma_with = lu_lemma.translate(table)
        lemmas.update([lemma_without, lemma_with])

    elif([char not in lu_lemma
          for char in ['(', ')', '[', ']']
          ]):
        lemmas.add(lu_lemma)
    else:
        raise Exception(f'problem processing {lu_lemma}')

    return lemmas

lemmas = lemmas_from_lu_name(lu_lemma='election')
assert lemmas == {'election'}

lemmas = lemmas_from_lu_name(lu_lemma='take (after)')
assert lemmas == {'take', 'take after'}

lemmas = lemmas_from_lu_name(lu_lemma="take (someone's) life")
assert lemmas == {'take life', "take someone's life"}

lemmas = lemmas_from_lu_name(lu_lemma='take [picture]')
assert lemmas == {'take', 'take picture'}








