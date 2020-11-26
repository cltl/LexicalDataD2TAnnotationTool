import sys
import pathlib
from nltk.corpus import framenet as fn

sys.path.append('../../')

import LexicalDataD2TAnnotationTool
from LexicalDataD2TAnnotationTool import create_lexicon_data_annotation_tool
from LexicalDataD2TAnnotationTool import add_frame_to_info
from LexicalDataD2TAnnotationTool import add_lu_to_info, add_lemma_to_pos_to_lu_urls

from FrameNetNLTK import load

cwd = pathlib.Path.cwd()
parent = cwd.parent

out_dir = f'{parent}/test/lexicon_data_for_frame_annotation_tool'
premon_nt_path = f'{parent}/res/premon/premon-2018a-fn17-noinf.nt'

create_lexicon_data_annotation_tool(path_readme=f'{parent}/doc/lexicon_data_for_frame_annotation_tool/README.md',
                                    path_ud_information=f'{parent}/doc/lexicon_data_for_frame_annotation_tool/part_of_speech_ud_info.json',
                                    path_mapping_ud_pos_to_fn_pos=f'{parent}/doc/lexicon_data_for_frame_annotation_tool/ud_pos_to_fn_pos.json',
                                    output_folder=out_dir,
                                    verbose=2)


add_frame_to_info(output_folder=out_dir,
                  fn_en=fn,
                  premon=LexicalDataD2TAnnotationTool.premon,
                  verbose=2)


add_lu_to_info(your_fn=fn,
               language='en',
               premon=LexicalDataD2TAnnotationTool.premon,
               namespace='http://rdf.cltl.nl/efn/',
               major_version=1,
               minor_version=7,
               output_folder=out_dir,
               verbose=2)

add_lemma_to_pos_to_lu_urls(output_folder=out_dir,
                            language='en',
                            verbose=2)

fn_nl = load('res/DutchFrameNet-0.1')

add_lu_to_info(your_fn=fn_nl,
               language='nl',
               premon=LexicalDataD2TAnnotationTool.premon,
               namespace='http://rdf.cltl.nl/dfn/',
               major_version=0,
               minor_version=1,
               output_folder=out_dir,
               verbose=2)

add_lemma_to_pos_to_lu_urls(output_folder=out_dir,
                            language='nl',
                            verbose=2)
