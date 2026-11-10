![Introduction banner: a pencil sprawled across the corner of a blank handled leaf, cotton gloves folded at the table rim, index drawers ajar behind and ribbon markers dangling from shelved tomes, no writing anywhere](intro-banner.png)

# dm-data-generalizer

Index entry, author leading: the name above is set in Caesar Dressing in post office blue, as an index card entry with a tiny date stamp portrait at the left of the title block and the pencil pictured once only, beside this opening heading.

![Logo](logo.png)

![Banner](banner.png)

![Animated scene](scene.svg)

![Major separator](sep-heavy.svg)

# dm-data-generalizer
Replaces specific data values with more general categories (e.g., replacing specific job titles with broader roles, or age with age ranges). - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

![Major separator](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowGuard-AI/dm-data-generalizer`

> Index memorandum: the README fetching line names an obsolete organisation.

![Minor separator](sep-light.svg)

## Usage
`python3 main.py input_file output_file [options]`

![Minor separator](sep-light.svg)

## Parameters
- `-h`: Show help message and exit
- `--job_title_column`: Name of the job title column to generalize
- `--age_column`: Name of the age column to generalize
- `--city_column`: Name of the city column to generalize to state
- `--num_rows`: Number of rows to process (optional, processes all if not specified)

> Index memorandum: an invocation lacking a column switch halts at exit 1 and produces nothing. It prints "No generalization column was specified."

![Minor separator](sep-light.svg)

## Behavior notes
- The output file may not be the input file. If the resolved output path is the input file, by the same spelling, a `./` alias, or a symlink, the run refuses at exit 1 before anything is written and the input is left untouched.
- At least one column flag must be given. A run with no column flag prints "No generalization column was specified.", exits 1, and writes no output file, instead of copying the input unchanged under a completion line.
- The city column is generalized with a built-in lookup table of well-known US cities, so the state written is the state that city is actually in: Chicago becomes Illinois, Houston becomes Texas, Los Angeles becomes California. The table is a fixed list in main.py (CITY_TO_STATE), matched without regard to case, so the same city maps to the same state on every row and every run. A city the table does not list becomes "Unknown", and the run logs a warning with the count of rows set to Unknown. No state is ever invented for a city the table does not know.

> Index memorandum: the destination may not resolve onto the source.

> Index memorandum: the geography dictionary fabricates no state for an unlisted place.

![Minor separator](sep-light.svg)

## License
This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

![Major separator](sep-heavy.svg)

## Cards filed at the table

The chief button of this re-skin reads Generalize the Values. Its row ceiling field label reads Rows to Process. Its safeguard heading reads The Output Is Never the Input. Its empty errand heading reads Name at Least One Column. It closes with the chamber at rest: pencil returned beside the twined bundle, drawers pushed shut, and widened entries filed under roomier headings than the ones they arrived wearing.
