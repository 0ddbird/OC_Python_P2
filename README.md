# BookWorm
## A webscraper for books.toscrape.com

## Installation

1. Clone the repository `git clone https://github.com/0ddbird/OC_Python_P2.git`
2. Navigate to the local directory `cd OC_Python_P2`
3. Create a virtual environment `python -m venv <venv_name>`
4. Activate the virtual environment `source <venv_name>/bin/activate`
5. Install requirements `pip install -r requirements.txt`
6. Execute the script `python -m src/main`

## Requirements

### Python version and cchardet

To run the most performant version of this script, Python 3.9.x is required.  
This version sets _cchardet_ over _charset-normalizer_ as an _aiohttp_ dependency.

If you want to use a later version of Python >= 3.10, don't install _cchardet_ package, _aiohttp_ will automatically switch to _charset-normalizer_.
 
### Parser options

Two parsers are available in this project.  
By default, the script will run using _Selectolax_.

If you prefer to use Beautiful Soup 4 instead, you can run `python -m src/main -bs4`

This project uses the _lxml_ parser over 'html.parser' for Beautiful Soup 4.
