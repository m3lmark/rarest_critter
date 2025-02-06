import requests
import concurrent.futures

user_id = "searching4critters"  # Replace with the actual user ID
taxon_frequency = {}

# Fetch species counts for the user
species_counts_url = "https://api.inaturalist.org/v2/observations/species_counts"
params = {
    "user_id": user_id,
    "fields": "taxon.name,taxon.rank,taxon.observations_count",
    "per_page": 100,
    "page": 1,
}

while True:
    response = requests.get(species_counts_url, params=params)
    if response.status_code == 200:
        data = response.json()
        for result in data["results"]:
            taxon_id = result["taxon"]["id"]
            observations_count = result["taxon"]["observations_count"]
            taxon_frequency[taxon_id] = observations_count
        if data["total_results"] <= params["page"] * params["per_page"]:
            break
        params["page"] += 1
    else:
        print(
            f"Error fetching species counts: {response.status_code} - {response.text}"
        )
        break

# Determine the top 5 taxa with the fewest total observations
sorted_taxa = sorted(taxon_frequency.items(), key=lambda item: item[1])[:5]


# Function to fetch taxon information and return common or scientific name
def fetch_taxon_info(taxon_id):
    taxon_url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}"
    response = requests.get(taxon_url)
    if response.status_code == 200:
        taxon_data = response.json()
        if "results" in taxon_data and len(taxon_data["results"]) > 0:
            common_name = taxon_data["results"][0].get("preferred_common_name")
            scientific_name = taxon_data["results"][0].get("name", "Unknown")
            name_to_print = common_name if common_name else scientific_name
            return taxon_id, name_to_print
    return taxon_id, "Unknown"


# Fetch taxon information for the top 5 rarest species in parallel
taxon_info = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(fetch_taxon_info, taxon_id) for taxon_id, _ in sorted_taxa
    ]
    for future in concurrent.futures.as_completed(futures):
        taxon_info.append(future.result())

# Sort the taxon information based on the original sorted order
taxon_info.sort(key=lambda x: sorted_taxa.index((x[0], taxon_frequency[x[0]])))

# Print the taxon information in order
for taxon_id, name in taxon_info:
    print(f"{name} (Taxon ID: {taxon_id}): {taxon_frequency[taxon_id]} observations")
