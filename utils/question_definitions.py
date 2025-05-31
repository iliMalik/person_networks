import pandas as pd

# Define the question table as a list of dictionaries
QUESTION_TABLE = [
    {"ID": 1, "question_id": "f2edcb18-d43e-4ea9-af1e-dde91e0cd03a", "question_text": "Have you often felt down, depressed, or hopeless?"},
    {"ID": 2, "question_id": "d04e7fea-6ba5-4d51-bf2f-fef016789382", "question_text": "Have you lost interest or pleasure in activities you usually enjoy?"},
    {"ID": 3, "question_id": "1634f65b-d58d-462e-b996-b91ee7931bc3", "question_text": "Have you felt unusually irritable or angry?"},
    {"ID": 4, "question_id": "27652b2c-e442-4c52-8405-b782a4dc2a44", "question_text": "Have you felt emotionally numb or detached from others?"},
    {"ID": 5, "question_id": "6b97503d-df5f-46b1-80b8-a8a4dff96b17", "question_text": "Have you had sudden mood swings or intense emotional reactions?"},
    {"ID": 6, "question_id": "c475d602-3a58-478c-8ee4-d3c5eea4bdae", "question_text": "Do you worry excessively about different things most days?"},
    {"ID": 7, "question_id": "39966f2f-a9ed-4a33-a7ec-b9173a9bae16", "question_text": "Do you often feel restless or on edge?"},
    {"ID": 8, "question_id": "1351c143-8212-46f4-8873-3553db1f23e3", "question_text": "Have you experienced sudden episodes of intense fear or panic?"},
    {"ID": 9, "question_id": "c5d6a97c-4dd2-4151-a010-50e37ce086e3", "question_text": "Do you avoid places or situations because they make you anxious?"},
    {"ID": 10, "question_id": "083bf6e8-cd9b-4c6b-a50a-48aa50177298", "question_text": "Have you experienced physical symptoms like racing heart, sweating, or shortness of breath without a medical cause?"},
    {"ID": 11, "question_id": "2a785af3-2fda-4a4e-9dcb-0a80e9bc6294", "question_text": "Have you found it hard to concentrate or make decisions?"},
    {"ID": 12, "question_id": "d537293a-b9ca-4eaa-9eb8-91a93e592776", "question_text": "Do you experience racing thoughts or feel like your mind won't slow down?"},
    {"ID": 13, "question_id": "76bec976-6261-449c-9f01-515f595c70fe", "question_text": "Have you had thoughts that others might find strange or illogical?"},
    {"ID": 14, "question_id": "a5001288-dc03-4240-af29-bd9c6cee08f4", "question_text": "Have you heard voices or seen things that others do not?"},
    {"ID": 15, "question_id": "9dbd6426-6cb9-47ed-8b9e-91ca65ebd31b", "question_text": "Do you believe others are watching, controlling, or trying to harm you?"},
    {"ID": 16, "question_id": "2bf56b66-735d-441c-9ceb-18c0fc9adb0d", "question_text": "Have you had trouble falling or staying asleep?"},
    {"ID": 17, "question_id": "88811111-0389-435e-bd91-297c1df1499e", "question_text": "Do you sleep too much or feel tired all the time despite sleeping?"},
    {"ID": 18, "question_id": "f5d26451-5410-4d0f-8fa8-25c8109cf368", "question_text": "Have you had unusual changes in energy levels (either very high or very low)?"},
    {"ID": 19, "question_id": "6201ec78-5927-4d71-8b83-32b185c4d8d2", "question_text": "Have you engaged in risky or impulsive behavior (spending, sex, driving, etc.)?"},
    {"ID": 20, "question_id": "19e5af06-e2b7-48b6-a91c-4df3304e88f1", "question_text": "Do you have difficulty controlling anger or aggressive urges?"},
    {"ID": 21, "question_id": "bf71cc92-fa0a-4011-8c4f-81656baf3c63", "question_text": "Have you used alcohol or drugs to cope with your feelings?"},
    {"ID": 22, "question_id": "baf20008-22a9-4c10-8deb-b51100aa236d", "question_text": "Do you experience unwanted, repetitive thoughts that cause you anxiety?"},
    {"ID": 23, "question_id": "df2acd55-abc5-46b2-aab0-17d64beb5ab3", "question_text": "Do you feel compelled to perform certain behaviors or rituals repeatedly?"},
    {"ID": 24, "question_id": "d829e732-8f86-432a-a66f-8c50d3bf0bcd", "question_text": "Do you feel distress if you cannot complete a ritual or habit?"},
    {"ID": 25, "question_id": "28d52d76-e8ff-4ec8-9cad-74e1cacb0358", "question_text": "Are you unhappy with your body or weight even if others say you are fine?"},
    {"ID": 26, "question_id": "6645874a-cab7-4b18-9735-fe2ef24a8998", "question_text": "Do you restrict food, overeat, or purge (vomit, use laxatives) to control weight?"},
    {"ID": 27, "question_id": "6ac5c290-5d60-4087-b936-63ae0d555f29", "question_text": "Have your eating habits significantly changed recently?"},
    {"ID": 28, "question_id": "f8e5944a-2653-4423-ab46-bdd1c183ae24", "question_text": "Have you experienced a traumatic event that still affects you?"},
    {"ID": 29, "question_id": "7676b45d-8acd-4865-9be7-60eb5735009e", "question_text": "Do you avoid reminders of something upsetting that happened to you?"},
    {"ID": 30, "question_id": "9301350e-ee02-48cc-a060-b890240efbdf", "question_text": "Do you have nightmares or flashbacks related to a past trauma?"},
    {"ID": 31, "question_id": "b3866674-6e20-4dee-80b5-4e63ade176bc", "question_text": "Is your mental health affecting your ability to work, study, or maintain relationships?"},
    {"ID": 32, "question_id": "beb93ee4-c1e8-48da-b65b-14cbd040046b", "question_text": "Do you find it difficult to manage daily tasks or responsibilities?"},
    {"ID": 33, "question_id": "8014156f-2f35-45b6-9046-0f380e9aa9c4", "question_text": "Have you thought about hurting yourself?"},
    {"ID": 34, "question_id": "9553ef9b-fecf-49dc-82a8-4ad6c1426679", "question_text": "Have you thought that life isn't worth living?"},
    {"ID": 35, "question_id": "85f96239-5082-4f33-9282-a4972eea37c2", "question_text": "Have you intentionally harmed yourself or attempted suicide?"}
]

# Create DataFrame
questions_df = pd.DataFrame(QUESTION_TABLE, columns=["ID", "question_id", "question_text"])