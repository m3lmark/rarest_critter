import requests
import concurrent.futures

user_id = "searching4critters"  # Replace with the actual user ID
species_type = "Mollusca"  # Replace with the desired species type
taxon_frequency = {}

# Fetch species counts for the user
species_counts_url = "https://api.inaturalist.org/v1/observations/species_counts"
params = {
    "user_id": user_id,
    "iconic_taxa": species_type,
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
            return name_to_print
    else:
        print(f"Error fetching taxon info: {response.status_code} - {response.text}")
        return None


# Fetch and display the common or scientific names of the top 5 taxa
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_taxon = {
        executor.submit(fetch_taxon_info, taxon_id): taxon_id
        for taxon_id, _ in sorted_taxa
    }
    results = []
    for future in concurrent.futures.as_completed(future_to_taxon):
        taxon_id = future_to_taxon[future]
        try:
            taxon_name = future.result()
            observations_count = taxon_frequency[taxon_id]
            results.append((taxon_name, taxon_id, observations_count))
        except Exception as exc:
            print(f"Error fetching taxon name for Taxon ID {taxon_id}: {exc}")

# Sort the results by the number of observations
results.sort(key=lambda x: x[2])

# Display the sorted results
for taxon_name, taxon_id, observations_count in results:
    print(f"{taxon_name} (Taxon ID: {taxon_id}): {observations_count} observations")
