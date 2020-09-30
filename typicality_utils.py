import os
import json
import copy
from operator import itemgetter

from .rdf_utils import get_rdf_uri, get_rdf_label

def initialize_typical_frames(output_folder,
                              fn_en,
                              premon,
                              event_type,
                              overwrite=False,
                              verbose=0):
    """
    initialize a JSON file mapping all frame URIs to zero
    (can be updated later with typicality scores)
    """
    typical_folder = os.path.join(output_folder, 'typicality')
    if not os.path.exists(typical_folder):
        os.mkdir(typical_folder)
    scores_folder = os.path.join(typical_folder, 'typicality_scores')
    if not os.path.exists(scores_folder):
        os.mkdir(scores_folder)

    event_type_path = os.path.join(scores_folder, f'{event_type}.json')
    if os.path.exists(event_type_path):
        if overwrite:
            if verbose >= 1:
                print(f'file for {event_type} exists, but will be overwritten')
        else:
            if verbose >= 1:
                print(f'file exists and will not be overwritten, exiting function.')
            return

    frame_uri_to_zero = {}
    for frame in fn_en.frames():
        label = frame.name

        frame_rdf_uri = get_rdf_uri(premon_nt=premon,
                                    frame_label=label)

        frame_uri_to_zero[frame_rdf_uri] = 0

    with open(event_type_path, 'w') as outfile:
        json.dump(frame_uri_to_zero,
                  outfile,
                  indent=4,
                  ensure_ascii=False,
                  sort_keys=True)

    if verbose:
        print(f'initialized event type typicality JSON at {event_type_path}')




def update_typical_frames(output_folder,
                          premon,
                          event_type,
                          frame_to_typicality,
                          frame_format='fn_label',
                          verbose=0):

    accepted_formats = {'fn_label', 'premon_frame_uri'}
    assert frame_format in accepted_formats, f'{frame_format}'

    typical_folder = os.path.join(output_folder, 'typicality')
    scores_folder = os.path.join(typical_folder, 'typicality_scores')
    if not os.path.exists(scores_folder):
        os.mkdir(scores_folder)

    event_type_path = os.path.join(scores_folder, f'{event_type}.json')
    if not os.path.exists(event_type_path):
        print(f'{event_type_path} does not exist, please first initialize.')
        return
    else:
        frame_to_score = json.load(open(event_type_path))

    for frame, score in frame_to_typicality.items():

        if frame_format == 'fn_label':
            rdf_uri = get_rdf_uri(premon_nt=premon,
                                  frame_label=frame)

        elif frame_format == 'premon_frame_uri':
            rdf_uri = frame
            assert rdf_uri.startswith('http://premon.fbk.eu/resource/'), f'you provided {rdf_uri}, but it should start with http://premon.fbk.eu/resource/'

        frame_to_score[rdf_uri] = score

    if verbose:
        print()
        print(f'updated: {event_type_path}')
        print(f'updated scores for {len(frame_to_typicality)} frames')

    with open(event_type_path, 'w') as outfile:
        json.dump(frame_to_score,
                  outfile,
                  indent=4,
                  ensure_ascii=False,
                  sort_keys=True)



def create_lexical_lookup_per_eventtype(event_type,
                                        language,
                                        premon,
                                        output_folder,
                                        overwrite=False,
                                        verbose=0):
    """
    create a JSON file mapping

    'ordered_frames'
        list of lists
        [
            [typicality_score, dropdown label, PreMOn URI],
            ..
        ]

    'lexical_lookup'
        LEMMA
            POS
                [typicality_score, dropdown label, PreMON frame URI, LU_NAME, LU_URI]
            'all_frames':
                [PreMOn frame URI, PreMOn URI, ...]

    :param str event_type: an event_type for which there exists typicality scores
    :param str language: supported: nl | en
    :param str output_folder: the main folder for the lexical data
    """
    lu_to_info_path = os.path.join(output_folder, 'lexicons', language, 'lu_to_info.json')
    assert os.path.exists(lu_to_info_path), f'no lexicon found for language ({language}). Please first create lu_to_info.json.'

    with open(lu_to_info_path) as infile:
        lu_to_info = json.load(infile)

    lemma_to_pos_to_lus_path = os.path.join(output_folder, 'lexicons', language, 'lemma_to_pos_to_lus.json')
    assert os.path.exists(lemma_to_pos_to_lus_path), f'no lexicon found for language ({language}). Please first create lemma_to_pos_to_lus.json.'

    with open(lemma_to_pos_to_lus_path) as infile:
        lemma_to_pos_to_lus = json.load(infile)

    event_type_path = os.path.join(output_folder, 'typicality', 'typicality_scores', f'{event_type}.json')
    assert os.path.exists(event_type_path), f'no typicality scores found for event type {event_type}'

    with open(event_type_path) as infile:
        frame_to_score = json.load(infile)

    lexical_lookup_dir = os.path.join(output_folder, 'typicality', 'lexical_lookup')
    if not os.path.exists(lexical_lookup_dir):
        os.mkdir(lexical_lookup_dir)

    lexical_lang_lookup_dir = os.path.join(lexical_lookup_dir, language)
    if not os.path.exists(lexical_lang_lookup_dir):
        os.mkdir(lexical_lang_lookup_dir)

    lexical_lookup_path = os.path.join(lexical_lang_lookup_dir, f'{event_type}.json')
    if all([os.path.exists(lexical_lookup_path),
                           not overwrite]):
        print(f'lexical look up path exists: {lexical_lookup_path}')
        print('will not overwrite it, exiting function')
        return


    # get frame uri -> frame label
    frame_uri_to_info = {}
    for frame_uri, score in frame_to_score.items():
        label = get_rdf_label(premon, frame_uri)
        frame_uri_to_info[frame_uri] = [score,
                                        f'{label} ({score})',
                                        frame_uri]

    # get ordered frames
    ordered_frames = list(frame_uri_to_info.values())
    ordered_frames.sort(key=itemgetter(0),
                        reverse=True)

    lemma_to_pos_to_dropdown = {}
    all_frames = set(frame_uri_to_info)
    assert len(all_frames) == 1221

    for lemma, pos_to_lu_uris in lemma_to_pos_to_lus.items():
        lemma_to_pos_to_dropdown[lemma] = {}
        frames_for_lemma = set()

        for pos, lu_uris in pos_to_lu_uris.items():

            values = []
            for lu_uri in lu_uris:

                lu_info = lu_to_info[lu_uri]
                lu_name = lu_info['lu_name']

                frame_uri = lu_info['frame_uri']
                frame_label = lu_info['frame_label']
                typicality_score = frame_to_score[frame_uri]

                dropdown_label = f'{frame_label} ({lu_name}) ({typicality_score})'

                values.append([typicality_score,
                               dropdown_label,
                               frame_uri,
                               lu_uri,
                               lu_name])

                frames_for_lemma.add(frame_uri)

            values.sort(key=itemgetter(0),
                        reverse=True)

            lemma_to_pos_to_dropdown[lemma][pos] = values

        # list of 'all_frames'
        lemma_to_pos_to_dropdown[lemma]['all_frames'] = list(frames_for_lemma)

    the_json = {
        'ordered_frames' : ordered_frames,
        'lexical_lookup' : lemma_to_pos_to_dropdown
    }

    with open(lexical_lookup_path, 'w') as outfile:
        json.dump(the_json,
                  outfile,
                  indent=4,
                  ensure_ascii=False,
                  sort_keys=True)

    if verbose:
        print(f'written lexical lookup for {event_type} to {lexical_lookup_path}')






