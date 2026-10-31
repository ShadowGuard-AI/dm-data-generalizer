![Banner](banner.png)

# dm-data-generalizer
Replaces specific data values with more general categories (e.g., replacing specific job titles with broader roles, or age with age ranges). - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

## Install
`git clone https://github.com/ShadowStrikeHQ/dm-data-generalizer`

## Usage
`./dm-data-generalizer [params]`

## Parameters
- `-h`: Show help message and exit
- `--job_title_column`: Name of the job title column to generalize
- `--age_column`: Name of the age column to generalize
- `--city_column`: Name of the city column to generalize to state
- `--num_rows`: Number of rows to process (optional, processes all if not specified)

## Behavior notes
- The output file may not be the input file. If the resolved output path is the input file, by the same spelling, a `./` alias, or a symlink, the run refuses at exit 1 before anything is written and the input is left untouched.
- At least one column flag must be given. A run with no column flag prints "No generalization column was specified.", exits 1, and writes no output file, instead of copying the input unchanged under a completion line.
- The city column is generalized with a built-in lookup table of well-known US cities, so the state written is the state that city is actually in: Chicago becomes Illinois, Houston becomes Texas, Los Angeles becomes California. The table is a fixed list in main.py (CITY_TO_STATE), matched without regard to case, so the same city maps to the same state on every row and every run. A city the table does not list becomes "Unknown", and the run logs a warning with the count of rows set to Unknown. No state is ever invented for a city the table does not know.

## License
Copyright (c) ShadowStrikeHQ
