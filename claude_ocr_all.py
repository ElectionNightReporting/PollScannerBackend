import logging

logging.basicConfig(
    filename='ocr_processing.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

headers = [
    'Election Header',
    'Close Polls Report',
    'Tally Report By Precinct',
    'Grand Blanc Township\nPrecinct 9',
    'Straight Party Ticket',
    'Electors of President and\n Vice-President of the\nUnited States',
    'United States Senator',
    'Representative in\n Congress\n 8th District',
    'Representative in State\n Legislature\n 72nd District',
    'Member of the State\n Board of Education',
    'Regent of the Univeristy of\n Michigan',
    'Trustee of Michigan State\n University',
    'Governor of Wayne State\n University',
    'Prosecuting Attorney',
    'Sheriff',
    'Clerk and Register of Deeds',
    'Treasurer',
    'Drain Commissioner',
    'Surveyor',
    'County Commissioner\n 5th District',
    'Supervisor',
    'Clerk',
    'Treasurer',
    'Trustee',
    'Justice of Supreme Court\n 8 Year Term',
    'Justice of Supreme Court\n Incumbent Position\n Partial Term Ending\n 01/01/2029',
    'Judge of Court of Appeals\n 2nd District\n Incumbent Position',
    'Judge of Court of Appeals\n 2nd District\n Non-Incumbent Position',
    'Judge of Circuit Court\n 7th Circuit\n Incumbent Position',
    'Judge of Circuit Court\n 7th Circuit\n Incumbent Position\n Partial Term Ending\n 01/01/2029',
    'Judge of Circuit Court\n 7th Circuit\n Non-Incumbent Position',
    'Judge of Probate Court\n Incumbent Position',
    'Judge of District Court\n 67th District, 4th Division\n Non-Incumbent Position',
    'Board of Trustee Member\n Molt Community College',
    'Grand Blanc Community\n Schools\n Board Member'
    'Precinct Ballot Count'
]

candidate_names = [
    "Democratic Party",
    "Republican Party",
    "Libertarian Party",
    "Green Party",
    "U.S. Taxpayers Party",
    "Working Class Party",
    "Natural Law Party",
    "Undervotes",
    "Overvotes",
    "Write-ins",
    "Kamala Harris",
    "Tim Walz",
    "Donald J. Trump",
    "JD Vance",
    "Chase Oliver",
    "Mike ter Maat",
    "Randall Terry",
    "Stephen E. Broden",
    "Robert F. Kennedy, Jr.",
    " Nicole Shanahan",
    "Joseph Kishore",
    "Jerry White",
    "Cornel West",
    "Melina Abdullah",
    "Elissa Slotkin",
    "Mike Rogers",
    "Joseph Solis-Mullen",
    "Dave Stein",
    "Douglas P. Marsh",
    "Doug Dern",
    "Curtis Hertel",
    "Tom Barrett",
    "L. Rachel Dailey",
    "Kristen McDonald Rivet",
    "Paul Junge",
    "Steve Barcelo",
    "James Allen Little",
    "Kathy Goodwin",
    "Jim Casha",
    "Anissa Buffin",
    "Phil Green",
    "Denise Illitch",
    "Shauna Ryder Diggs",
    "Carl Meyers",
    "Sevag Vartanian",
    "Andrew Chadderdon",
    "Donna M. Oetman",
    "Rebecca Bahar-Cook",
    "Thomas Stallworth",
    "Mike Balow",
    "Julie Maday",
    "Grant T. Baker",
    "Janet M. Sanger",
    "John Paul Sanger",
    "John Anthony La Pietra",
    "Mark T. Gaffney",
    "Rasha Demashkieh",
    "Busuito, Michael",
    "Reddy, Sunny",
    "Farid Ishac",
    "William Mohr II",
    "Suzanne Roehrig",
    "Sami Makhoul",
    "Kathleen Oakford",
    "David Leyton",
    "Christopher R. Swanson",
    "Jeff Salzeider",
    "Domonique Clemons",
    "Sam E. Muma",
    "Brenda Duplanty",
    "Ashley Witte",
    "Carrie K. Bock",
    "Patrick Gerace",
    "Michael Link",
    "Monica Shapiro",
    "Scott Bennett",
    "Jet Kilmer",
    "David B. Robertson",
    "Mike Yancho Sr.",
    "Bob Brundle",
    "Sarah Hugo",
    "Paul J. White",
    "Jude Rariden",
    "Kevin Harmes",
    "Joel Feick",
    "Parker Wheatley",
    "Lonnie Adkins",
    "Cecelia Adkins",
    "Coetta Adams",
    "Steve Schlicht",
    "Karen L. Jones",
    "Gary Keeler",
    "Jerry Cole",
    "Sam Spence",
    "Fred Christensen",
    "Jim Coon",
    "Steven Shaski II",
    "Larry Green",
    "Scott DeSilva",
    "DeWayn Allen",
    "Jona May Kean",
    "Pamala Green",
    "Michele Loper",
    "Dora King",
    "Brian S. Baxter",
    "Reginald P. Mays",
    "Tonya Ketzler",
    "Jennifer Arrand Stainton",
    "Cory Jo Bostwick",
    "Danelle Barker",
    "Kimberly Jimenez",
    "Debra J. Ridley",
    "Mark T. Gorton",
    "Dan Morey",
    "Kyle Ward",
    "Leah Davis",
    "Zach Sack",
    "Joseph M. Madore",
    "Teri Webber",
    "Cheryl Campbell-Hoberg",
    "Brian G. Arnes",
    "Gerald Masters",
    "Keith J. Pyles",
    "John W. Minto",
    "Don Harris",
    "Justin J. Layman",
    "Brandon S. Davis",
    "Tammy Batterbee",
    "Rachel A. Stanke",
    "Richard L. Russell",
    "Stacey Wells",
    "Kristine M. Taylor",
    "John A. Congdon",
    "Susan L. Guith",
    "Janis A. Franich",
    "Theo Gantos",
    "Eric Gunnels",
    "Jeremy Kline",
    "Tim Brenner",
    "Patrick Tack",
    "Joseph A. Rizk",
    "Cynthia J. Bryan",
    "Cathrine A. Thompson",
    "Richard T. Johnson",
    "Jeffrey Thomas",
    "Sue Thomas",
    "Sheryllynn Russo",
    "Karin J. Muron",
    "Jeffery Harrington",
    "Andrew Fink",
    "Kimberly Ann Thomas",
    "Kyra Harris Bolden",
    "Patrick William O'Grady",
    "Adrienne Nicole Young",
    "Randy J. Wallace",
    "NP  Mary Hood",
    "NP  Nancy K. Chinonis",
    "Ariana E. Heath",
    "Jeffrey E. Clothier",
    "Amanda Odette",
    "Leon El-Alamin",
    "Carol McIntosh",
    "Danielle N. Cusson",
    "Liz Armstrong",
    "Denise Miller",
    "Greg Jones",
    "Ray M. Culbert",
    "Lawrence W. Allen Jr.",
    "Jerry Link",
    "Thomas Hicks",
    "Colleen Brown",
    "Thomas J. Banks",
    "Aaron J. Burch",
    "Lori Machuk",
    "Melissa Hoose",
    "Scott Webster",
    "Robert Arnold",
    "Andrea Martin",
    "Wayne Walter",
    "Michael Withey",
    "David A. Krueger",
    "John A. Gilbert",
    "Walter M. Melen",
    "Connie Greene",
    "Valerie DeLauter",
    "Ronda Roach",
    "Stephanie Saintmarie",
    "David Lucik",
    "Sherry Ann Moore",
    "Jonathan D. Schlinker",
    "Melissa Schluentz",
    "Barbara BakerOmerod",
    "Geraldine Terry",
    "Larry Widigan",
    "David Campbell",
    "Keith St. Clair",
    "Paul Terry",
    "Byron Vowell",
    "John Ray",
    "Rick Ferguson",
    "Vadice Burgett III",
    "Terry Gill",
    "Ana M. Lerma",
    "Mechelle Valley",
    "Perci Whitmore",
    "Anne Figueroa",
    "Andrew Watchorn",
    "Gail L. Johnson",
    "Amanda Wares",
    "Aron Gerics",
    "Jeffrey R. Swanson",
    "Andy Everman",
    "Kenyetta V. Dotson",
    "Richard Wagonlander",
    "Candice Miller",
    "Virginia A. Sepanak",
    "Mary Davis",
    "Jenna Rose Marden",
    "Bette Bigsby",
    "Craig Lanter",
    "Katrina Royster",
    "Calvin Clemmons",
    "Charles Robinson",
    "Johnnie Reed",
    "Jan Bugbee",
    "Rene Robbins",
    "David Love",
    "Steven L. Bentley",
    "Cheryl L. Blosser",
    "Hayley Downs",
    "Kevin W. Burge",
    "Tony Howard",
    "Toby J. Bauldry",
    "David Cook",
    "Cynthia Parker",
    "Katie Barnum",
    "Phillip Hamilton",
    "Jeanette Prestonise",
    "Tonia Ritter",
    "Gloria Nealy",
    "Gary Cousins",
    "Carrie Ammons",
    "Bob Gaffney",
    "Robert J. Love",
    "Dawn Renkiewicz",
    "Robert D. Love",
    "Benjamin Vick",
    "Shannon McKee",
    "Robert Malcomnson",
    "Sherry Marden",
    "Connie Green",
    "Matt Smith",
    "Holly Halabicky",
    "Diane Rhines",
    "Maggie Miller",
    "Corey A. Herriman",
    "Kasey J. Fiebernitz",
    "Darrick Huff",
    "Ky Orvis",
    "Andrew Younger",
    "John W. Jordan",
    "Brian Eltringham",
    "Dana Jones",
    "Laura Setzke",
    "Chad Schlosser",
    "Linda K. Boose",
    "Janice Winkiel",
    "Megan LeCureux",
    "John Ferguson",
    "Gary O'Hare",
    "Virginia Riggs",
    "Patrick Tesler",
    "Greg Main",
    "Ashley Herriman",
    "Ethan J. Lang",
    "Kelly Ryckaert",
    "Maureen Callahan",
    "Richard E. Hill",
    "Charles A. Wade",
    "Kevin Brown",
    "Justin Schweigert",
    "Heidi Howieson",
    "Sevinc Sparks",
    "Vickie Lee Luoma",
    "Richard G. Gulledge",
    "Shantell Bennett",
    "John H. Rynearson",
    "Katie O'Dell",
    "Tabitha Ramberg",
    "Lauren Dooley",
    "James C. Henderson Jr.",
    "Rachel Millington",
    "Darci Sherman",
    "Gary Shreve",
    "Herbert Thompson",
    "Trevor Jones",
    "Barry Gross",
    "Charles Wright",
    "Vicki VanCura",
    "Dan Hill",
    "Russell Edwards",
    "Mary D. Severn",
    "Amy Plyler",
    "Stephanie Rowe",
    "Arlene Wilborn",
    "Jerry A. Birchmeier Jr.",
    "Adam Green",
    "Jon Henige",
    "Joseph M. Henige",
    "Jay Kuchar",
    "Joseph M. Toma",
    "Jennifer Otter",
    "Alyssa A. Bouchard",
    "Carrie Germain",
    "Jessica Lanave",
    "Holly Jarvis",
    "Autumn Henry",
    "Lester Fykes",
    "Tyra Coburn",
    "Cherese Bransford",
    "Jessie B. Cloman Sr.",
    "Kimberly Turner",
    ]

# Flag duplicate if the header is already in the JSON and the first corresponding text is the same
# Since there could be cases where the header is the same but the text is different, we need to check the first corresponding text

import json
import time
import anthropic
import base64
import os
from pathlib import Path
from difflib import SequenceMatcher

def similar_strings(a, b, threshold=0.85):
    if a is None or b is None:
        return False
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

def process_ocr(frames_dir: Path):
    # Initialize anthropic client and load schemas
    client = anthropic.Anthropic()
    
    with open('schema_null.json', 'r') as f:
        schema_null = f.read()

    final_schema = json.loads(schema_null)

    # Prepare all images - modified to sort by timestamp
    image_paths = sorted(frames_dir.glob('*.jpg'), 
                        key=lambda x: float(x.stem.split('_')[1]))

    counter = 0
    for image_path in image_paths:
        with open('schema.json', 'r') as f:
            schema = f.read()

        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()

        logging.info(f"Processing {image_path.name}...")

        # Create the message with all images
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            temperature=0,
            system="""You are a world-class OCR machine. 
            Given multiple images, fill out the JSON schema only with the provided text. 
            Fill out what you can, but do not make up values that are not in the images. 
            DO NOT CREATE NEW KEYS IN THE SCHEMA. 
            IMPORTANT: If you cannot detect a contest title, do not include any contest data in the results.
            It is a given that some of the schema fields can not be filled out.""",
            messages=[
                {
                "role": "user",
                "content": [{
                    "type": "text", 
                    "text": f"""Please fill out this JSON schema with the OCR data from the image. Give me the JSON only.

    For reference:
    1. The headers appear in this exact order in the images: {headers}
    2. Only these candidate names will appear in the images: {candidate_names}
        a. There are NO OTHER CANDIDATE NAMES that will appear in the images. Therefore if the name by OCR 
        is similar to the candidate names but off by a few characters, then it is the SAME CANDIDATE.

    Schema to fill out:
    {schema}"""
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64.b64encode(image_data).decode()
                    }
                }
                ]
            },
            {
                    "role": "assistant",
                    "content": "Here is the JSON requested:\n{"
            }]
        )

        schema = message.content[0].text
        logging.info("\n\n\nschema: \n%s", schema)

        output_json = json.loads("{" + message.content[0].text)
        logging.info("\n\n\noutput_json: \n%s", output_json)

        try:
            for key in output_json.keys():    
                if key == "results" and "contests" in output_json["results"]:
                    for contest in output_json["results"]["contests"]:
                        # Error check if claude hallucinated
                        if "title" in contest:
                            contest_title = contest["title"]
                            # Check for duplicate contest
                            idx_in_final_schema = -1
                            try:
                                # Look for similar contest titles instead of exact match
                                for idx, c in enumerate(final_schema["results"]["contests"]):
                                    logging.info(f"Checking contest at index {idx}")
                                    logging.info(f"c['title']: {c.get('title')}")
                                    logging.info(f"contest_title: {contest_title}")
                                    
                                    if ("title" in c and c["title"] is not None and 
                                        similar_strings(c["title"], contest_title)):
                                        logging.info(f"Found contest {contest_title} at index {idx} in final schema")
                                        idx_in_final_schema = idx
                                        break
                            except Exception as e:
                                logging.error(f"Error in finding contest {contest_title} in final schema: {e}")
                                pass

                            if idx_in_final_schema != -1:
                                contest_from_schema = final_schema["results"]["contests"][idx_in_final_schema]

                                # Check if there are candidates in the contest
                                if contest["candidates"] and contest_from_schema["candidates"]:
                                    first_candidate_name_from_claude = contest["candidates"][0]["ticket"][0]
                                    first_candidate_name_from_schema = contest_from_schema["candidates"][0]["ticket"][0]
                                    # Check for similar candidate names instead of exact match
                                    if similar_strings(first_candidate_name_from_claude, first_candidate_name_from_schema):
                                        # Add the candidates to the final schema that are not already in the final schema
                                        for candidate in contest["candidates"]:
                                            # Check if similar candidate name exists
                                            if not any(similar_strings(candidate["ticket"][0], existing["ticket"][0]) 
                                                     for existing in contest_from_schema["candidates"]):
                                                contest_from_schema["candidates"].append(candidate)
                                        if "metadata" in contest:
                                            for metadata_key in contest["metadata"].keys():
                                                # Add metadata if it is not already in the final schema
                                                if "metadata" not in contest_from_schema:
                                                    contest_from_schema["metadata"] = {}
                                                if metadata_key not in contest_from_schema["metadata"]:
                                                    contest_from_schema["metadata"][metadata_key] = contest["metadata"][metadata_key]
                                        logging.info(f"Updating contest {contest_title} in final schema")
                                        continue
                                    else:
                                        logging.info(f"Candidate names do not match for contest {contest_title}")
                                        logging.info(f"\tCandidate names from claude: {first_candidate_name_from_claude}")
                                        logging.info(f"\tCandidate names from schema: {first_candidate_name_from_schema}")
                                        # Check if candidate exists in any contest in final schema
                                        if first_candidate_name_from_claude in [c["candidates"][0]["ticket"][0] for c in final_schema["results"]["contests"]]:
                                            logging.info(f"\tContest {contest_title} is a duplicate of a duplicate in the final schema")
                                            continue
                                else:
                                    logging.info(f"No candidates in contest {contest_title}")
                                    continue
                            else:
                                logging.info(f'Contest {contest_title} not found in final schema')

                            logging.info(f"Adding contest {contest_title} to final schema")
                            final_schema["results"]["contests"].append(contest)
                else:
                    # Non-contest fields
                    if key in final_schema:
                        # If the key exists and is a dictionary, update it recursively
                        if isinstance(final_schema[key], dict) and isinstance(output_json[key], dict):
                            logging.info(f"Updating {key} in final schema")
                            final_schema[key].update(output_json[key])
                        # Otherwise just replace the value
                        else:
                            logging.info(f"Adding {key} to final schema")
                            final_schema[key] = output_json[key]
                    else:
                        logging.info(f"Adding {key} to final schema")
                        final_schema[key] = output_json[key]
        except Exception as e:
            logging.error("-"*50)
            logging.error(f"Error in combining schemas: {e}")
            logging.error("-"*50)
        
        time.sleep(1)
        # counter += 1
        # if counter > 5:
        #     break

    logging.info("\n\n\nfinal_schema: \n%s", final_schema)

    # Change the output path to be in the same directory as the images
    output_path = frames_dir / 'final_schema.json'
    with open(output_path, 'w') as f:
        json.dump(final_schema, f)

    return final_schema