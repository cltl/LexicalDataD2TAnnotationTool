# Lexical data annotation tool

The goal of this package is to create the lexical data that is used in https://github.com/cltl/frame-annotation-tool.

## Prerequisites
Python 3.6 was used to create this project. It might work with older versions of Python.

## Installing
A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```

## Resources
Please call install.sh to download the relevant resources.
```bash
bash install.sh
```

## Usage

### Function 1: create folder with lexical data

This will copy the data in doc/lexicon_data_for_frame_annotation_tool
into your requested output folder.

```python 

from LexicalDataDTDAnnotationTool import create_lexicon_data_annotation_tool

create_lexicon_data_annotation_tool(path_readme='LexicalDataDTDAnnotationTool/doc/lexicon_data_for_frame_annotation_tool/README.md',
                                    path_ud_information='LexicalDataDTDAnnotationTool/doc/lexicon_data_for_frame_annotation_tool/part_of_speech_ud_info.json',
                                    path_mapping_ud_pos_to_fn_pos='LexicalDataDTDAnnotationTool/doc/lexicon_data_for_frame_annotation_tool/ud_pos_to_fn_pos.json',
                                    output_folder='LexicalDataDTDAnnotationTool/test/lexicon_data_for_frame_annotation_tool',
                                    verbose=2)
```

### Function 2: add frame information
Once the folder has been created, you can add a file containing information about the frames
using:

```python 
import LexicalDataDTDAnnotationTool,
from LexicalDataDTDAnnotationTool import add_frame_to_info
from nltk.corpus import framenet as fn

add_frame_to_info(output_folder='LexicalDataDTDAnnotationTool/test/lexicon_data_for_frame_annotation_tool',
                  fn_en=fn,
                  premon=LexicalDataDTDAnnotationTool.premon,
                  verbose=0)
```
This will add the file **frame_to_info.json** to the output folder.

### Function 3: add language-specific lexicon information
The next step is to add language-specific lexicon information

```python
import LexicalDataDTDAnnotationTool
from LexicalDataDTDAnnotationTool import add_lu_to_info
from nltk.corpus import framenet as fn

add_lu_to_info(your_fn=fn,
               language='en',
               premon=LexicalDataDTDAnnotationTool.premon,
               namespace='http://rdf.cltl.nl/',
               major_version=1,
               minor_version=7,
               output_folder=out_dir,
               verbose=2)
```
The function will create one file in the output folder at:
```
lexicons:
    LANGUAGE
        lu_to_info.json

with the structure
lu_url (created based on the provided namespace)
    attributes of the lexical unit
 ```

## Function 4: mapping lemma to pos to lu_url

After running step 3, there is a file called *lu_to_info.json*
for each language. 
You can also generate a mapping from a lemma to a POS to the lu urls by calling the following function.
```
from LexicalDataDTDAnnotationTool import add_lemma_to_pos_to_lu_urls

add_lemma_to_pos_to_lu_urls(output_folder=out_dir,
                            language='nl',
                            verbose=2)
```

This will add *lemma_to_pos_to_lus.json* to the lexicon folder of the language.

### Function 5: add/update typicality frame scores

#### Function 5a: initialize typicality frame score

```python
from nltk.corpus import framenet as fn
import LexicalDataDTDAnnotationTool
from LexicalDataDTDAnnotationTool import initialize_typical_frames

initialize_typical_frames(output_folder='LexicalDataDTDAnnotationTool/test/lexicon_data_for_frame_annotation_tool',
                          fn_en=fn,
                          premon=LexicalDataDTDAnnotationTool.premon,
                          event_type='Q40231',
                          overwrite=False, # if False, will not be initialized if the file exists
                          verbose=2)
```
This will create a file at **typicality/typicality_scores/Q40231.json** containing a mapping from a PreMOn frame URI -> typicality score.
All scores are zero at this stage. The next function allows users to update the typicality scores.

#### Function 5b: update typicality frame scores

```python
import LexicalDataDTDAnnotationTool
from LexicalDataDTDAnnotationTool import update_typical_frames


frame_to_typicality = {
    'http://premon.fbk.eu/resource/fn17-change_of_leadership' : 0.8,
}

update_typical_frames(output_folder='LexicalDataDTDAnnotationTool/test/lexicon_data_for_frame_annotation_tool',
                      premon=LexicalDataDTDAnnotationTool.premon,
                      event_type='Q40231',
                      frame_to_typicality=frame_to_typicality,
                      frame_format='premon_frame_uri',
                      verbose=2)
```

This will update the JSON file with the scores as provided by frame_to_typicality.
You can choose between two formats (see **frame_format**): fn_label | premon_frame_uri.

#### Function 6: create lexical lookup per event type

It is possible to create a lexical lookup per event type.

```python

import LexicalDataDTDAnnotationTool

from LexicalDataDTDAnnotationTool import create_lexical_lookup_per_eventtype

create_lexical_lookup_per_eventtype(event_type='Q40231',
                                    language='nl',
                                    premon=LexicalDataDTDAnnotationTool.premon,
                                    output_folder='LexicalDataDTDAnnotationTool/test/lexicon_data_for_frame_annotation_tool',
                                    overwrite=True,
                                    verbose=2)

```

Provided that there exist:
* typicality scores for the event type 'Q40231' in the specified language
* lexical information about the language

This function will generate a JSON file at typicality/lexical_lookup/LANGUAGE/EVENT_TYPE.json with the following format:
```
'ordered_frames'
        list of lists
        [
            [PreMOn URI, dropdown label, typicality_score],
            ..
        ]

    'lexical_lookup'
        LEMMA
            POS
                [typicality_score,
                 dropdown_label,
                 frame_uri,
                 lu_uri,
                 lu_name,
                 lexicon_url]
            'all_frames':
                [PreMOn frame URI, PreMOn URI, ...]
```

## Authors
* **Marten Postma** (m.c.postma@vu.nl)

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
