from .process_essay import grade_batch, save_results
from .reader import read_files
import re
import numpy as np
import csv


filepath = "/Users/hyw/Documents/NTU/112-2/計算語言學/FinalProject/essay-judge/essay"

instruction = """
Content: 
Point 5-4 : Excellent to very good: well-stated thesis related to the assigned topic with relevant, substantive, and detailed supports 
Point3: Good to average: limitedly-developed or vague thesis with irrelevant statements 
Point2-1: Fair to poor: poorly-developed or obscured thesis; too much repetition of limited relevant sentences 
Point0: Very poor: not pertinent; or no written products

Organization: 
Point 5-4 : Excellent to very good: well-organized structure with beginning, development, and ending; effective transition with logical sequencing and coherence
Point3: loosely-organized structure with imbalanced beginning, development, and ending; less effective transition that obvious affects logical sequencing and coherence
Point2-1: choppy ideas scattering without logical sequencing and coherence
Point0: no organization, no sequencing and coherence; or not pertinent

Grammar and rhetoric: 
Point 5-4 : Excellent to very good: well-structured sentences with variety; appropriate rhetoric; few grammatical errors 
Point3: less well-structured sentence with some errors of tense, agreement, etc.; but meaning seldom obscured
Point2-1: major errors of conjunctions, fragments, or ill-structured sentences that make meaning confused or obscured 
Point0: no organization, no sequencing and coherence; or not pertinent

Vocabulary: 
Point 5-4 : Excellent to very good: specific and effective wording; idiomatic and no spelling error
Point3: : dull and repeated wording; occasional errors of word/idiom form, choice, usage but meaning not obscured
Point2-1: : inappropriate wording; frequent spelling errors; meaning confused or obscured
Point0: some relevant words found, but meaning incomprehensible

給分的形式請使用「總分：分數」。
"""


def extract_score(description, pattern=r'總分：(\d+)'):
    # Define a regular expression pattern to match the score
    match = re.search(pattern, description)

    if match:
        return int(match.group(1))
    else:
        return None


def get_scores(filepath, instruction):
    batch_scores = []
    for result in grade_batch(filepath, instruction):
        score = extract_score(result['grade_content'])
        batch_scores.append(score)
        print(score)

    return batch_scores


print("Batch 1:")
scores_batch1 = get_scores(filepath, instruction)
print("Batch 2:")
scores_batch2 = get_scores(filepath, instruction)

# File name for the CSV
filename = 'scores.csv'

# Writing to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header (optional)
    writer.writerow(['Batch1', 'Batch2'])

    # Write the data
    for item1, item2 in zip(scores_batch1, scores_batch2):
        writer.writerow([item1, item2])

print(f"Data has been written to {filename}")

# plt.scatter(scores_batch1, scores_batch2)
print(
    f"The correlation between the two grade batches are: {np.corrcoef(scores_batch1, scores_batch2)[0, 1]}")
