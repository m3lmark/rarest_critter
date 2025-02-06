# Rarest Critters

## Description

This script fetches the species counts for a specified user from the iNaturalist API and determines the top 5 taxa with the fewest total observations (the rarest "critters"). It then fetches and displays the common name if applicable, otherwise using the scientific name.

## Prerequisites

- Python 3.x
- `requests` library

## Installation

You can install the `requests` library using pip:

```sh
pip install requests
```

## Usage

1. Replace the `user_id` variable with the actual username of the iNaturalist user you want to fetch data for.

2. Run the script:

```sh
python rarest_critter.py
```

## Script Details

The script performs the following steps:

1. Fetches species counts for the specified user from the iNaturalist API.
2. Determines the top 5 taxa with the fewest total observations.
3. Fetches taxon information (common or scientific name) for these taxa in parallel using a thread pool.
4. Displays the taxon information along with the number of observations.

## Example Output

```sh
Golden Bolete (Taxon ID: 363581): 389 observations
Johnny Cash Tarantula (Taxon ID: 501065): 447 observations
Red-mantle Saddle-back Tamarin (Taxon ID: 1368627): 482 observations
Kelp Scallop (Taxon ID: 192642): 597 observations
Coopers Chiton (Taxon ID: 130884): 683 observations
```

## Notes

- The script uses the iNaturalist API to fetch species counts and taxon information.
- The script fetches taxon information in parallel to improve performance.
- If the common name is not available, the script uses the scientific name.

