import requests
import pandas as pd
import os

def download_fda_data(output_dir="csvs_baixados"):
    """
    Download all the CSV files from the FDA and concatenate them.
    """
    urls = [
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/c7d0b43c-7250-4809-8a05-fcde5862f076",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d4f29180-7c76-40ac-9341-cf62702c4090",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f136b41b-56f3-43a9-9d6a-61b2afca5b4a",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/e0b11800-8922-11df-b3d7-0002a5d5c51b",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/a83f0b99-9038-4c5a-aaac-8792b32838fe",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/63d5cd82-02e3-4436-b81a-12d45bb6a90b",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/5e9a8ff0-3fdf-448a-97b3-83e6b904d864",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/2d33d9ae-1fe6-477e-9285-8890f6e98be4",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/7baa7ebb-cb08-4799-80d4-66c16966d223",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1a87f53c-0c8a-4c66-9048-2a0cf60a6a5c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/db0c7f7c-7624-477d-ab7c-310a903c7025",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/a41b7601-34f2-4a88-a406-f53011fb7de1",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/ce88effe-7ff2-418f-acb3-3cb5d5d2bf95",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/06f34d0f-4e72-41d3-967f-8abf3f2005c1",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/48c86164-de07-4041-b9dc-f2b5744714e5",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f96b315c-fa57-4876-a7e5-a9b584d8e6e6",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d19d59cb-f1cd-479d-ab0c-a36971e65544",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/280ee057-3488-4d77-b510-8bc733eeca1e",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f8b2634b-ccd7-4a42-8db3-26ba9e9627e6",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/6b5f89e9-1292-4f13-5590-44c874bf299c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/76798bc5-6752-4c02-9f03-68a361eea66b",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/b63c4c7d-3dbf-419d-84cc-2c1957b92be7",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/67d5c665-ca88-49ba-b7d3-7145d9878cf0",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/de16dd6a-859b-4180-c6af-f930be14f26a",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/76504ed2-6417-4176-bc31-24eccb8b5584",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/3ed8472a-c6eb-4076-9d66-025ede589e3d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/9dff46c6-4b15-4d10-aca6-d5ef3735a530",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/745ff8df-1618-4b76-9aa1-6f42752c0dda",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/8143d01c-4911-40db-95b2-47f3ebea2a7d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/18e8f9fc-4d62-4d30-4ab7-bac03336171e",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/dad367dd-7cb8-4344-9920-8710149473d2",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f9499a4d-1288-4bd3-9d59-1d72092c38cd",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/7df68090-7e98-4b01-9c29-0b941a1c307d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/618a7f1b-7162-4d16-9076-51b8aab4c8d2",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/135ff1b4-c21f-4df1-97be-9475680e9e44",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/63d283dd-e857-4c0e-b1fa-9e9d9b8717a8",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1a8b7b47-d5f8-e6b5-e063-6394a90a9ac4",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/89191ae9-7f2b-4206-8397-bf7fce3436ac",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/2ec65f7e-4aa2-4b41-b578-885ea59d6e9d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/b5bd99e4-569d-48d5-ba75-16e69f8c409a",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/36e9a878-d6c2-4808-9915-294f47b1fe3d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/dcecf9e0-6c28-4964-9ddb-9379705fa26c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/47ef5267-5624-48d4-91e2-483e93755f6f",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f1ad4bca-839d-41cd-a132-a6984780912e",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/e80cfadc-71b6-4881-b5f7-2be67adbf8b8",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/9a4037a2-6c63-457a-8d6f-2fd05d926ea2",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/618db7b8-a5e4-49c8-9390-38912e6f39fd",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d61c7f99-438b-4cac-ae10-997ff4c0fd1f",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1a8b8271-208d-ecde-e063-6294a90a54c6",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/a21f4f4b-b891-4f25-b747-cb9ec7d865d6",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1a545aab-fb4a-3f42-e063-6294a90a8351",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d099cf95-a7cc-4636-994d-226c3f866cdc",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/8355d971-d377-4d1d-973e-a65798bce7f9",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/30952400-0572-4431-9150-3a41affffb9a",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/ab802261-3eeb-4eea-af6a-31c830ac91f8",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/fc5cfd1c-1ff5-4cfa-b544-db8d7f26d46f",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/3513dfb0-4d62-4ad1-bb15-75c7555896ff",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/29b794b9-f503-edf4-e063-6394a90aef42",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/81758772-80b1-4e76-8f50-e68d1fb4e9ee",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/05822ec0-a82a-11e7-81fe-424c58303031",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1adcb911-4e6b-7b6f-e063-6394a90a8264",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/29b78835-6a39-54ad-e063-6294a90a82cb",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/5fe0ce14-bc11-4b43-b002-7efdca0d3003",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/de0e2089-f781-4d47-99f5-c2a1b7b0f1eb",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/03f2c9fc-534b-49ec-9113-81938b1eadb9",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/8213c229-a67a-4d3f-bd8f-b8729ae28472",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/96ca1b4c-67bf-3db6-24c5-c4841b073c66",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/ced9a8b6-ef2c-a620-c61c-ff9374249543",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d041603b-fa96-433c-a9bc-5393aab4a289",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/64f608b7-ad43-4395-b806-d4216175c8d3",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/9dbbf304-7be3-4417-8285-a8f5fd20f977",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/a06c4ead-c988-4b10-b832-4d7460fa358f",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/67de8652-2e5a-4d18-aee9-d9b789ccfe46",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/0c3cd915-babe-49c0-8aac-bf0247a17f3e",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/0d4af785-f5e8-4f6e-91f6-2ece6ab58d5c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/6d9b6c87-784e-4f8a-8c82-1a7a97193337",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/61d4995d-92be-4678-74b9-79b3e12e5e30",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/dccfb747-8f64-46ec-3993-95195b585581",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/276b84fb-096b-3f91-e054-00144ff8d46c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/e654303b-b7b1-4e5b-a0a1-e999110060bf",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/b68b7911-628d-4932-b0e8-4ae72c48f92f",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/95c6fdb6-b587-4413-92f9-d592b9f7a23e",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/252968ca-c714-4c1c-9e60-0b699cb9362f",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/2abf71cb-5c02-c5af-e063-6394a90a34b1",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/0a9e384f-e717-436b-b9a0-15e53cef0862",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/73eae9fc-507b-4c9c-883d-63eb2e3cc6f6",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/6b2c9ee3-ae88-46f1-9b3f-fc9e9e716cbf",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/2dc730d5-55fd-4e98-8c8a-daa7d8f872b0",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/bcaf5f75-caaf-41fd-875b-5800310070d1",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/fd5652b6-5ae4-437e-a456-47deaf500794",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/530786f0-58d9-4370-88f0-6e98e4b85183",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/4d8781ff-9366-462c-8161-6e958f44fcb4",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/ab1c3318-578e-4d0c-a21e-fc6df07e9fb7",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/6046583d-f1a5-4620-80bc-03992b6525d0",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f70cf2fc-6e6d-4a74-9f7a-db8fec072fd7",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/5b237fbc-d58a-4ca0-a56b-f9425d14dab5",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/5d49181b-b974-a5da-3b38-12a3a87bb96b",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/e8c6b638-c22f-4c20-ba40-b9d5e85c9541",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1158fa93-ef41-4a29-8252-9251f94c53c8",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d4e2cf51-e6a8-4103-bb1d-6120c6474ff8",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/3a33a84f-166b-4698-90b9-d79265234ae7",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1a264c2f-d2f8-4ab5-bc5e-fbed0001ede6",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/bb362a20-6d91-4ae8-bebb-9ee8b2591814",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/4c97c74d-b6b5-4492-b7ed-e02c76cc8514",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/4c6db457-2514-48b9-b48a-fa6258aba116",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/34a647f5-8728-451b-b918-94c8acd15974",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/6979f24b-5f49-4190-a4e6-c1523e0d3108",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/84b7a672-eeb1-4527-84ac-68196b156be2",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/fd2f21f0-9f8e-4abd-b603-e1834a252c2d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/ba8d4e72-f452-4859-ae6f-3644b4b0a78c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/be18292e-b1a2-4815-a0ed-003efaa6bea3",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/e5c837e7-41e8-496a-9c85-6b0453b35948",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/1e50f275-002e-413f-a840-66ee3cb3740c",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/f3182470-1965-4e20-dbaf-e3506f893ea5",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/aaf3b24e-85fd-43ee-b657-2ee4df312ec3",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/5f674a82-00fb-41f8-99a5-df8985771324",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/21b75f1d-1cda-49e5-8176-cc23827824f3",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/ad1fbe7f-2995-45dd-92f3-7baccaab85d9",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/168a670b-0cbb-067c-e054-00144ff88e88",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/09d800e3-427e-4973-9261-61592d662bbd",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/194fde77-eaf8-4e4c-84ef-35d67b5eec11",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/613aaac9-ec18-4b22-addb-599e1193e6f5",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/70bfb8c1-6d1a-4b0a-8a21-7a7ed8e748c9",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/cd98bff9-4602-4268-d68d-029a14a5513b",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/46993726-584e-4907-ac4d-94e59b236b82",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/c3c03458-942c-4565-8a9c-1901bb0d2db0",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/da102644-62a9-41c2-8a91-6fc19a03e6f1",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/69fc3841-a461-4706-bdcb-1176c40bf486",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/d3a52eba-83d2-4fd1-8db5-dd04bcb1ba9d",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/524cf052-e90e-4595-af0a-608edbe9bd31",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/b557ec63-3599-4372-b4f8-ea022b4e3712",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/2b1db7a1-c3f2-42e5-8499-91724edbf65e",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/0280849d-5c78-4a9d-8941-4eab429f6bd8",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/279a251c-f4d0-4c47-b999-7ef1a45ac0d0",
    "https://nctr-crs.fda.gov/fdalabel/services/meddra/sec-terms-csv/e9ba0102-8cbb-4c4c-810e-292119095a8a"
]

    dataframes = []
    os.makedirs(output_dir, exist_ok=True)

    for i, url in enumerate(urls):
        response = requests.get(url)
        if response.status_code == 200:
            caminho_csv = os.path.join(output_dir, f"arquivo_{i}.csv")
            with open(caminho_csv, "wb") as f:
                f.write(response.content)
            df = pd.read_csv(caminho_csv)
            dataframes.append(df)
        else:
            print(f"Error when downloading {url}")

    df_final = pd.concat(dataframes, ignore_index=True)
    return df_final

def filter_adverse_reactions(df):
    """
    Filter only the adverse reactions section and remove irrelevant terms.
    """
    df_reac = df[df['Section'] == 'ADVERSE REACTIONS SECTION'].copy()

    words_to_remove = [
    "Adverse event", "Adverse reaction", "Immunization", "Immunisation", "COVID-19",
    "Hepatitis B", "Hepatitis A", "Injection", "Pregnancy", "Pregnant",
    "Vaccination", "Revaccination", "Immunisation reaction", "Immunization reaction",
    "COVID-19 immunisation", "COVID-19 vaccination", "Cardiac catheterization",
    "Cardiac MRI", "Magnetic resonance imaging heart", "Diabetes", "Diabetes mellitus",
    "Hospitalisation", "Hospitalization", "Illness", "Medication error", "Oral contraceptive",
    "Oral contraception", "Protein total", "Protein", "Surgery", "Surgical intervention",
    "Blind", "Blindness", "Crying", "Fall", "Infant", "Pneumonia", "Type 2 diabetes mellitus",
    "Asthma", "Mumps", "Rubella", "Measles", "Polymerase chain reaction", "Tetanus",
    "Varicella", "Clubbing", "Pain assessment", "HIV infection", "Immunocompromised",
    "Immunodeficiency", "Immunosuppression", "Body surface area", "Lymphocyte count",
    "Neutrophil count", "Vaccine viraemia", "Blood potassium", "Blood sodium", "pH body fluid",
    "Skin exfoliation", "Scales", "Mass", "Caregiver", "HIV positive", "HIV test positive",
    "Viral load", "Anaesthesia", "Chest X-ray", "Brief resolved unexplained event",
    "Road traffic accident", "Diabetes mellitus insulin-dependent", "Type 1 diabetes mellitus",
    "Food allergy", "Elderly", "Nasal septal operation", "Haemorrhoid operation", "Prostatism",
    "Analgesic drug level", "Body temperature", "Drainage", "Alcoholism", "Investigation",
    "Poliomyelitis", "Bed rest", "Rest regimen", "COVID-19 immunisation", "Alcohol use",
    "C-reactive protein", "Rabies", "Delivery", "Glucose tolerance impaired", "In vitro fertilization",
    "Stillbirth", "Blood chloride normal", "Weight", "Magnetic resonance imaging", "Blood insulin",
    "Biopsy skin", "Chemotherapy", "Renal transplant", "Diphtheria", "Pertussis", "Typhoid fever", "Yellow fever", "Anthrax", "Smallpox",
    "H1N1 influenza", "Dengue fever", "Herpes zoster meningitis", "Pulmonary tuberculosis",
    "Vaccinia virus infection", "Varicella zoster virus infection", "Prophylaxis", "Electrocardiogram", "Electrocardiogram ST segment elevation",
    "Electrocardiogram T wave abnormal", "Electrocardiogram T wave inversion",
    "Electrocardiogram abnormal", "Biopsy", "Blood phosphorus", "Brain natriuretic peptide", "Blood chloride", "Troponin increased",
    "Blood immunoglobulin G", "Platelet count", "Red blood cell sedimentation rate",
    "Blood creatine phosphokinase", "Blood creatine phosphokinase increased", "Blood aluminium",
    "Blood lead", "Troponin", "Troponin I", "Alanine aminotransferase increased",
    "Blood creatinine", "Globulin", "Body mass index", "Hypercholesterolaemia", "Hypertension", "Dyslipidaemia", "Gout",
    "Osteoarthritis", "Vitiligo", "Multiple sclerosis", "Thyroid cancer", "Breast cancer",
    "Nasopharyngeal cancer", "Lung adenocarcinoma", "Pancreatic carcinoma", "Adenocarcinoma",
    "Neoplasm malignant", "Foreign body", "Overdose", "Alcohol poisoning", "Chemical poisoning",
    "Craniocerebral injury", "Head injury", "Limb injury", "Wrist fracture",
    "Completed suicide", "Suicide attempt"]

    df_reac['LLT_temp'] = df_reac['Occurring LLT'].str.split('\\').str[-1].str.strip()

    mask_llt = ~df_reac['LLT_temp'].isin(words_to_remove)
    mask_pt = ~df_reac['PT'].isin(words_to_remove)

    df_filtrado = df_reac[mask_llt & mask_pt].copy()

    return df_filtrado.drop(columns=['LLT_temp'])

def save_data(df, filename):
    """Save the dataframe as a CSV file with the appropriate encoding."""
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"File {filename} saved successfully!")