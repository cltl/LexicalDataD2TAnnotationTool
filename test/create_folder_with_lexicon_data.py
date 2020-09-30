import sys
import pathlib
from nltk.corpus import framenet as fn

sys.path.append('../../')

import LexicalDataDTDAnnotationTool
from LexicalDataDTDAnnotationTool import create_lexicon_data_annotation_tool
from LexicalDataDTDAnnotationTool import add_frame_to_info
from LexicalDataDTDAnnotationTool import add_lu_to_info, add_lemma_to_pos_to_lu_urls

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
                  premon=LexicalDataDTDAnnotationTool.premon,
                  verbose=2)


add_lu_to_info(your_fn=fn,
               language='en',
               premon=LexicalDataDTDAnnotationTool.premon,
               namespace='http://rdf.cltl.nl/',
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
               premon=LexicalDataDTDAnnotationTool.premon,
               namespace='http://rdf.cltl.nl/',
               major_version=0,
               minor_version=1,
               output_folder=out_dir,
               verbose=2)

add_lemma_to_pos_to_lu_urls(output_folder=out_dir,
                            language='nl',
                            verbose=2)
