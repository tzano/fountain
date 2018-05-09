# Fountain 

Fountain is a natural language data augmentation tool that helps developers create and expand domain specific chatbot training datasets for machine learning algorithms.

# Overview.

In order to build better AI assistants, we need more data, better models aren’t enough.

Most of NLU system requires entering thousands of possible queries that future users would -- most possibly -- use, and annotate every sentence segment that can identiy user's intentions. It is generally a hectic and tedious manual process. Fountain aims to help developers smooth away this process and generate a volume of training examples to make it easier to train and build a robust chatbot systems. 

The tool intends to make it easy to build the same dataset for different intent engines (Amazon's Alexa, Google's API.ai, Facebook's Wit, Microsoft's Luis). At the moment, the tool generates training datasets compatible with the RasaNLU format.


## Getting Started

### Installation
You can install the package via:
```sh
$ pip install git+git://github.com/tzano/fountain.git
```
Install the dependencies:
```sh
$ pip install -r requirements.txt
```

### Syntax

Fountain uses a structured `YAML` template, developers can determine the scope of intentions through the `template`  with the grammar definitions. Every intent should include at least one `sample utterances` that triggers an action. The query includes attributes that identify user's intention. These key information called `slots`. We include different samples to be able to generate datasets.

We use three operations:
- Argument (`{slot_name:slot_type}`): used to declare slot pattern.
- Argument (`( first_word | second_word )`): used to provide a set of keywords, these words could be synonymes (e.g: happy, joyful) or the same name with different spellings (e.g: colors|colours) 

A simple example of an intent would be like the following
```
book_cab:
  - utterance: Book a (cab|taxi) to {location:place}
    slots:
      location:place:
        - airport
        - city center
```

This will generate the following intent `json file` using `to_json`.
```
[
    {
        "entities": [
            {
                "end": 21, 
                "entity": "location", 
                "start": 14, 
                "value": "airport"
            }
        ], 
        "intent": "book_cab", 
        "text": "book a cab to airport"
    }, 
    {
        "entities": [
            {
                "end": 25, 
                "entity": "location", 
                "start": 14, 
                "value": "city center"
            }
        ], 
        "intent": "book_cab", 
        "text": "book a cab to city center"
    }, 
    {
        "entities": [
            {
                "end": 22, 
                "entity": "location", 
                "start": 15, 
                "value": "airport"
            }
        ], 
        "intent": "book_cab", 
        "text": "book a taxi to airport"
    }, 
    {
        "entities": [
            {
                "end": 26, 
                "entity": "location", 
                "start": 15, 
                "value": "city center"
            }
        ], 
        "intent": "book_cab", 
        "text": "book a taxi to city center"
    }
]
```

The same file would generate the following  `csv file` using `to_csv`.
```
intent	utterance
book_cab	book a cab to airport
book_cab	book a cab to city center
book_cab	book a taxi to airport
book_cab	book a taxi to city center
```


### Builtin 
The library supports several pre-defined slot types (entities) to simplify and standardize how data in the slot is recognized.

These entities have been collected from different open-source data sources. 

- Dates, and Times
    - `FOUNTAIN:DATE`
    - `FOUNTAIN:WEEKDAYS`
    - `FOUNTAIN:MONTH_DAYS`
    - `FOUNTAIN:MONTHS`
    - `FOUNTAIN:HOLIDAYS`
    - `FOUNTAIN:TIME`
    - `FOUNTAIN:NUMBER`

- Location
    - `FOUNTAIN:COUNTRY`
    - `FOUNTAIN:CITY`

- People 
    - `FOUNTAIN:FAMOUSPEOPLE`

### Data Sources
In order to build `Fountain's` builtin datatypes, we processed data from the following data sources: 

- [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) WikiData 
- [GeoNames](http://www.geonames.org/) Geographical database 
- [Pantheon dataset](http://pantheon.media.mit.edu/rankings/people/US/all/-4000/2010/H15)

### How to use it:

You can easily load and parse DSL template and export the generated dataset ([Rasa format](https://github.com/RasaHQ/rasa_nlu)).

You can find this sample under the directory [`\labs`](/labs)

```
# DataGenerator
data_generator = DataGenerator()
# load template
template_fname = '<file>.yaml'
# parse the DSL template
results = data_generator.parse(template_fname)

# export to csv file
data_generator.to_csv('results.csv')
# export to csv file
data_generator.to_json('results.json')
```

# Test

```
pytest
```

# Tutorials & Guides 

You can find examples on how to use the library in `labs` folder. You can enrich the builtin datasets by adding more files under `data/<language>/*files*.csv`. Make sure to index the files that you insert in `resources/builtin.py`.

For more information about Chatbots and Natural Language Understanding, visit one of the following links: 

- [RASA NLU](https://github.com/RasaHQ/rasa_nlu)
- [Voice Design Guide](https://developer.amazon.com/designing-for-voice/) - A great resource for learning conversational and voice user interface design.

# Platforms 
- RASA NLU (Supported)

# Projects that used Fountain:
- [Wren - News Chatbot](https://github.com/tzano/wren/tree/master/wren/data) to discover & explore daily news stories. We used `Fountain` to generate more than 20,000 samples. The [Yaml](https://github.com/tzano/wren/tree/master/wren/data) file is available [here](https://github.com/tzano/wren/tree/master/wren/data).

## Support
If you are having issues, please let us know or submit a pull request.

## License
The project is licensed under the MIT License.