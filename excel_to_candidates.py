import pandas as pd

# df = pd.read_excel('nov5_genesee_county_candidate_list.xlsx')

df = pd.read_excel('nov5_genesee_county_candidate_list.xlsx', skiprows=2)

columns = df.columns
column_name_to_index = {column: index for index, column in enumerate(columns) if column != f"Unnamed: {index}"}

candidates = []
counter = 0
# President + vice president
for row in df.itertuples():
    # print(row)
    row = row[column_name_to_index["CANDIDATE"] + 1]
    if pd.notna(row):
        names = row.split("/")
        if len(names) > 1:
            candidates.extend([name.strip() for name in names])
        else:
            candidates[-1] = candidates[-1] + " " + names[0].strip()
    counter += 1
    if counter > 16:
        break

for row in list(df.itertuples())[17:]:
    candidate_name = row[column_name_to_index["CANDIDATE"] + 1]
    if pd.notna(candidate_name) and candidate_name != "CANDIDATE":
        candidates.append(candidate_name.strip())

for candidate in candidates:
    print('"' + candidate + '",')
