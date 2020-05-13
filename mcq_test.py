

questions = [
    {
        "id": "1",
        "question": "A 42-year-old female presents for follow-up after being treated for recurrent respiratory problems at an urgent care facility. She is feeling a little better after a short course of oral prednisone and use of an albuterol (Proventil, Ventolin) inhaler. She has had a gradual increase in shortness of breath, a chronic cough, and a decrease in her usual activity level over the past year. She has brought a copy of a recent chest radiograph report for your review that describes panlobular basal emphysema. She does not have a history of smoking, secondhand smoke exposure, or occupational exposures. Spirometry in the office reveals an FEV1/FVC ratio of 0.67 with no change after bronchodilator administration.\nWhich one of the following underlying conditions is the most likely cause for this clinical presentation?",
        "answers": ["1-Antitrypsin deficiency", "Bronchiectasis"," Diffuse panbronchiolitis", "Interstitial lung disease", "Left heart failure"], 
        "correct": "a"
    },
    {
        "id": "2",
        "question": "An otherwise healthy 57-year-old male presents with mild fatigue, decreased libido, and erectile dysfunction. A subsequent evaluation of serum testosterone reveals hypogonadism.\nWhich one of the following would you recommend at this time?",
        "answers": ["No further diagnostic testing","A prolactin level", "A serum iron level and total iron binding capacity", "FSH and LH levels", "Karyotyping"],
        "correct": "d"
    }
]

#print (questions[0]["question"])
anslabels = ['a', 'b', 'c', 'd', 'e']
correct = 0 
x = "*"*10 + " ABFM 2019 ITE Question " + "*"*10
print (x + "\n" + "*" * (len(x)))

for q in questions:
    print (q['question'])
    x = 0 
    for ans in q['answers']:
        print(anslabels[x] + ": " + ans)
        x += 1
    input_answer = input("\nType a, b, c, or e to select your answer. Then press ENTER.\n")
    if (input_answer == q["correct"]): 
        correct += 1
    print("\n")

score = correct/len(questions) * 100
print (f"Your final score is {score}%!")