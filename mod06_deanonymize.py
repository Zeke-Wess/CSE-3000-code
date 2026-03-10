import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df:pd.DataFrame, aux_df:pd.DataFrame):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    
    unique_anon = anon_df.drop_duplicates(subset=["age", "zip3", "gender"], keep=False) # Remove any duplicates 
    unique_aux = aux_df.drop_duplicates(subset=["age", "zip3", "gender"], keep=False)
    unique_anon.sort_values(by=["age", "zip3", "gender"], inplace=True)       # Sort so the names will line up 
    unique_aux.sort_values(by=["age", "zip3", "gender"], inplace=True)
    matches = pd.DataFrame({"anon_id": unique_anon["anon_id"], "matched_name" : unique_aux["name"]})
    return matches

def deanonymization_rate(matches_df:pd.DataFrame, anon_df:pd.DataFrame):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return (matches_df["anon_id"].size) / (anon_df["anon_id"].size)
