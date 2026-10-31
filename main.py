import argparse
import logging
import sys
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Data generalization mappings (can be extended)
JOB_TITLE_MAPPING = {
    "Software Engineer": "Engineer",
    "Data Scientist": "Data Analyst",
    "Project Manager": "Manager",
    "Accountant": "Finance Professional",
    "Teacher": "Educator",
    "Nurse": "Healthcare Professional",
    "Doctor": "Healthcare Professional",
    "Lawyer": "Legal Professional",
    "Sales Representative": "Sales Professional",
    "Marketing Manager": "Marketing Professional"
}

# City to state lookup for well-known US cities. Every pairing here is
# a plain fact checked against the city itself, not a generated value.
# A city that is not in this table generalizes to "Unknown" instead of
# being given a state it may not be in; see generalize_city_to_state.
CITY_TO_STATE = {
    "new york": "New York",
    "new york city": "New York",
    "los angeles": "California",
    "chicago": "Illinois",
    "houston": "Texas",
    "phoenix": "Arizona",
    "philadelphia": "Pennsylvania",
    "san antonio": "Texas",
    "san diego": "California",
    "dallas": "Texas",
    "austin": "Texas",
    "jacksonville": "Florida",
    "fort worth": "Texas",
    "san jose": "California",
    "columbus": "Ohio",
    "charlotte": "North Carolina",
    "indianapolis": "Indiana",
    "san francisco": "California",
    "seattle": "Washington",
    "denver": "Colorado",
    "washington": "District of Columbia",
    "nashville": "Tennessee",
    "oklahoma city": "Oklahoma",
    "el paso": "Texas",
    "boston": "Massachusetts",
    "las vegas": "Nevada",
    "portland": "Oregon",
    "detroit": "Michigan",
    "louisville": "Kentucky",
    "memphis": "Tennessee",
    "milwaukee": "Wisconsin",
    "baltimore": "Maryland",
    "albuquerque": "New Mexico",
    "tucson": "Arizona",
    "sacramento": "California",
    "atlanta": "Georgia",
    "kansas city": "Missouri",
    "miami": "Florida",
    "minneapolis": "Minnesota",
    "cleveland": "Ohio",
    "tampa": "Florida",
    "st. louis": "Missouri",
    "st louis": "Missouri",
    "pittsburgh": "Pennsylvania",
    "cincinnati": "Ohio",
    "orlando": "Florida",
    "salt lake city": "Utah",
    "madison": "Wisconsin",
    "raleigh": "North Carolina",
    "oakland": "California",
    "fresno": "California",
}

# Cities seen in the current run that the lookup does not know, in the
# order they were seen. main reads this after the city column is applied
# so the run can warn with the count.
UNKNOWN_CITIES = []

AGE_RANGES = [
    (0, 17),
    (18, 25),
    (26, 35),
    (36, 45),
    (46, 55),
    (56, 65),
    (66, 75),
    (76, 85),
    (86, 95),
    (96, 120)
]

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Data Generalization Tool")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    parser.add_argument("--job_title_column", help="Name of the job title column to generalize", default=None)
    parser.add_argument("--age_column", help="Name of the age column to generalize", default=None)
    parser.add_argument("--city_column", help="Name of the city column to generalize to state", default=None) # Example of added feature
    parser.add_argument("--num_rows", type=int, help="Number of rows to process (optional, processes all if not specified)", default=None) # New Feature for only processing 'n' rows
    return parser

def generalize_job_title(job_title):
    """
    Generalizes a specific job title to a broader category.

    Args:
        job_title (str): The job title to generalize.

    Returns:
        str: The generalized job title, or the original if no mapping is found.
    """
    if job_title in JOB_TITLE_MAPPING:
        return JOB_TITLE_MAPPING[job_title]
    else:
        return job_title  # Return original if no mapping

def generalize_age(age):
    """
    Generalizes a specific age to an age range.

    Args:
        age (int): The age to generalize.

    Returns:
        str: The age range the age falls into, or "Unknown" if invalid age.
    """
    try:
        age = int(age)  # Ensure age is an integer
        if not 0 <= age <= 120:  # Basic sanity check
            return "Unknown" # Or raise an Exception
        for age_range in AGE_RANGES:
            if age_range[0] <= age <= age_range[1]:
                return f"{age_range[0]}-{age_range[1]}"
        return "Unknown" # In case age is not in the ranges provided
    except ValueError:
        logging.error(f"Invalid age value: {age}.  Returning 'Unknown'")
        return "Unknown"

def generalize_city_to_state(city):
    """
    Generalizes a city name to the state that city is in, using the
    built-in CITY_TO_STATE lookup table.

    Args:
        city (str): The city name.

    Returns:
        str: The true state for a city in the lookup table, matched
        without regard to case or surrounding spaces, or "Unknown" for
        a city the table does not list. The lookup is a plain table,
        so the same city maps to the same state on every row and
        every run.
    """
    state = CITY_TO_STATE.get(str(city).strip().lower())
    if state is None:
        UNKNOWN_CITIES.append(str(city))
        return "Unknown"
    return state

def main():
    """
    Main function to read input data, generalize specified columns, and write to output.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # The output may not name the input file, in any spelling. Resolved
    # paths are compared, so a symlink alias is caught as well as the
    # same string. Refuse before any write.
    if Path(args.output_file).resolve() == Path(args.input_file).resolve():
        logging.error("Output file must not be the input file. Choose a different output path.")
        sys.exit(1)

    # A run that names no column generalizes nothing, so it must not
    # copy the input to the output under a completion line.
    if not args.job_title_column and not args.age_column and not args.city_column:
        print("No generalization column was specified.")
        sys.exit(1)

    try:
        # Read the input CSV file
        df = pd.read_csv(args.input_file)

        # Limit number of rows if specified
        if args.num_rows is not None:
            df = df.head(args.num_rows)

        # Generalize job titles if specified
        if args.job_title_column:
            if args.job_title_column not in df.columns:
                raise ValueError(f"Job title column '{args.job_title_column}' not found in input file.")
            df[args.job_title_column] = df[args.job_title_column].astype(str).apply(generalize_job_title)

        # Generalize ages if specified
        if args.age_column:
            if args.age_column not in df.columns:
                raise ValueError(f"Age column '{args.age_column}' not found in input file.")
            df[args.age_column] = df[args.age_column].apply(generalize_age)

        # Generalize cities to states if specified (added feature)
        if args.city_column:
            if args.city_column not in df.columns:
                raise ValueError(f"City column '{args.city_column}' not found in input file.")
            UNKNOWN_CITIES.clear()
            df[args.city_column] = df[args.city_column].astype(str).apply(generalize_city_to_state)
            if UNKNOWN_CITIES:
                logging.warning(
                    f"{len(UNKNOWN_CITIES)} row(s) held a city the lookup does not know "
                    f"and were set to Unknown: {', '.join(sorted(set(UNKNOWN_CITIES)))}"
                )

        # Write the modified DataFrame to the output CSV file
        df.to_csv(args.output_file, index=False)
        logging.info(f"Data generalization complete. Output written to {args.output_file}")

    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Usage examples:
# python main.py input.csv output.csv --job_title_column "Job Title" --age_column "Age"
# python main.py input.csv output.csv --city_column "City"
# python main.py input.csv output.csv --job_title_column "Job Title" --num_rows 100