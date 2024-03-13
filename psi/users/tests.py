def plutchick(answers):
    if len(answers) != 92 or any(response not in [0, 1] for response in answers):
        return 'error answers count'
    # Категории и их индексы вопросов в тесте
    categories = {
        "vit": [6, 11, 31, 34, 36, 41, 55, 73, 77, 92],
        "reg": [2, 5, 9, 13, 27, 32, 35, 40, 50, 54, 62, 64, 68, 70, 72, 75, 84],
        "zam": [8, 10, 19, 21, 25, 37, 49, 58, 76, 89],
        "otr": [1, 20, 23, 26, 39, 42, 44, 46, 47, 63, 90],
        "pro": [12, 22, 28, 29, 45, 59, 67, 71, 78, 79, 82, 88],
        "kom": [3, 15, 16, 18, 24, 33, 52, 57, 83, 85],
        "gip": [17, 53, 61, 65, 66, 69, 74, 80, 81, 86],
        "rac": [4, 7, 14, 30, 38, 43, 48, 51, 56, 60, 87, 91]
    }

    results = {category: 0 for category in categories}

    for category, question_indices in categories.items():
        results[category] = round(sum(answers[i - 1] for i in question_indices) / len(question_indices) * 100)

    total_stress = sum(answers) / 92 * 100
    results['vse'] = round(total_stress)

    # Определение доминирующей категории
    dominant_category = max(results, key=results.get)

    return results


def tomas(answers):
    if len(answers) != 30 or any(response not in [0, 1] for response in answers):
        return 'error answers count'

    # Ключ для анализа ответов (0 соответствует 'A', 1 соответствует 'B')
    keys = {
        'Competition': {'0': [3, 8, 10, 17, 25, 28], '1': [6, 9, 13, 14, 16, 22]},
        'Collaboration': {'0': [5, 11, 14, 19, 20, 23], '1': [2, 8, 21, 26, 28, 30]},
        'Compromise': {'0': [2, 4, 13, 22, 26, 29], '1': [7, 10, 12, 18, 20, 24]},
        'Avoidance': {'0': [1, 6, 7, 9, 12, 27], '1': [5, 15, 17, 19, 23, 29]},
        'Accommodation': {'0': [15, 16, 18, 21, 24, 30], '1': [1, 3, 4, 11, 25, 27]}
    }

    # Подсчет ответов для каждой категории
    results = {style: 0 for style in keys}
    for i, response in enumerate(answers):
        response_key = str(response)  # Конвертируем 0 или 1 в строку '0' или '1'
        for style, answer_keys in keys.items():
            if (i + 1) in answer_keys[response_key]:
                results[style] += 1

    return results


def CJO(answers):

    if len(answers) != 20 or any(response not in [1, 2, 3, 4, 5, 6, 7] for response in answers):
        return 'error answers count'

    sub_scales = {
        "goals_in_life": [2, 3, 9, 15, 16, 17],  # 1-based indices: 3, 4, 10, 16, 17, 18
        "process_of_life": [0, 1, 3, 4, 6, 8],  # 1-based indices: 1, 2, 4, 5, 7, 9
        "result_of_life": [7, 8, 9, 11, 19],  # 1-based indices: 8, 9, 10, 12, 20
        "locus_of_control_self": [0, 14, 15, 18],  # 1-based indices: 1, 15, 16, 19
        "locus_of_control_life": [6, 9, 10, 13, 17, 18],  # 1-based indices: 7, 10, 11, 14, 18, 19
    }

    map1 = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

    obr = [1, 4, 5, 6, 9, 12, 13, 14, 17, 18, 19]

    scores = {key: 0 for key in sub_scales}

    # Calculate scores
    for i, answer in enumerate(answers):

        if i in obr:
            answer = map1[answer]

        for sub_scale, items in sub_scales.items():
            if i in items:
                scores[sub_scale] += answer

    return scores


def MIS(answers):

    if len(answers) != 110 or any(response not in [0, 1] for response in answers):
        return 'error answers count'

    key = {
        1: ([1, 3, 9, 48, 53, 56, 65], [21, 62, 86, 98]),
        2: ([7, 24, 30, 35, 36, 51, 52, 58, 61, 73, 82], [20, 80, 103]),
        3: ([43, 44, 45, 74, 76, 84, 90, 105, 106, 108, 110], [109]),
        4: ([2, 5, 29, 41, 42, 50, 102], [13, 18, 34, 85]),
        5: ([8, 16, 39, 54, 57, 68, 70, 73, 100], [15, 26, 31, 46, 83]),
        6: ([6, 32, 33, 55, 89, 93, 95, 101, 104], []),
        7: ([10, 12, 17, 28, 40, 49, 63, 72, 77, 79, 97], []),
        8: ([4, 11, 22, 23, 27, 38, 47, 59, 64, 67, 69, 81, 91, 94, 99], []),
        9: ([14, 19, 25, 37, 60, 66, 71, 78, 87, 92], [])
    }

    # Инициализируем словарь для подсчета совпадений по шкалам
    raw_scores = {i: 0 for i in range(1, 10)}

    # Подсчитываем "сырые" баллы для каждой шкалы
    for scale, (agree_questions, disagree_questions) in key.items():
        agree_score = sum(answers[q - 1] for q in agree_questions)
        disagree_score = sum(1 - answers[q - 1] for q in disagree_questions)
        raw_scores[scale] = agree_score + disagree_score

    # Создаем таблицу перевода "сырых" баллов в стены
    conversion_table = {
        1: [0, 1, 2, 3, "4-5", "6-7", 8, 9, 10, 11],
        2: ["0-1", 2, "3-4", "5-6", "7-9", 10, "11-12", 13, 13, 14],
        3: ["0-1", 2, 3, "4-5", 6, 7, 8, "9-10", 11, 12],
        4: [0, 1, 2, "3-4", 5, "6-7", 8, 9, 10, 11],
        5: ["0-1", 2, 3, "4-5", "6-7", 8, "9-10", 11, 12, "13-14"],
        6: ["0-1", 2, "3-4", 5, "6-7", 8, 9, 10, 11, 12],
        7: [0, 1, 2, 3, "4-5", 6, "7-8", 9, 10, 11],
        8: [0, 0, "1-2", "3-4", "5-7", "8-10", "11-12", 13, 14, 15],
        9: [0, 1, 2, "3-4", 5, 6, 7, 8, 9, 10]
    }


    # Интерпретируем "сырые" баллы для каждой шкалы
    interpretation = {}
    for scale, raw_score in raw_scores.items():
        sten = None
        for i, interval in enumerate(conversion_table[scale]):
            if isinstance(interval, int) and raw_score == interval:
                sten = i + 1
            elif isinstance(interval, str):
                low, high = map(int, interval.split('-'))
                if low <= raw_score <= high:
                    sten = i + 1
        interpretation[scale] = sten

    return interpretation


def leongard(answers):
    if len(answers) != 88 or any(response not in [0, 1] for response in answers):
        return 'error answers count'

    # Define the questions for each scale, '1' for 'yes' adds to the score, '0' for 'no'
    questions_for_scale = {
        "Гипертимность (Г)": {"yes": [1, 11, 23, 33, 45, 55, 67, 77], "no": [], 'kof': 3},
        "Дистимность (В)": {"yes": [9, 21, 43, 74, 87], "no": [31, 53, 65], 'kof': 3},
        "Циклотимность (Ц)": {"yes": [6, 18, 28, 40, 50, 62, 72, 84], "no": [], 'kof': 3},
        "Возбудимость (В)": {"yes": [8, 20, 30, 42, 52, 64, 75, 86], "no": [], 'kof': 3},
        "Застревание (З)": {"yes": [2, 15, 24, 34, 37, 56, 68, 78, 81], "no": [12, 46, 59], 'kof': 2},
        "Эмотивность (Эм)": {"yes": [3, 13, 35, 47, 57, 69, 79], "no": [25], 'kof': 3},
        "Экзальтированность (Эк)": {"yes": [10, 32, 54, 76], "no": [], 'kof': 6},
        "Тревожность (Т)": {"yes": [6, 27, 38, 49, 60, 71, 82], "no": [5], 'kof': 3},
        "Педантичность (П)": {"yes": [4, 14, 17, 26, 36, 48, 58, 61, 70, 80, 83], "no": [39], 'kof': 2},
        "Демонстративность (Де)": {"yes": [7, 19, 22, 29, 41, 44, 63, 66, 73, 85, 88], "no": [51], 'kof': 2},
    }

    results = {}
    for scale, questions in questions_for_scale.items():
        score = sum(answers[q - 1] for q in questions["yes"]) + sum(1 - answers[q - 1] for q in questions["no"])
        results[scale] = score * questions['kof']

    return results


def HMI(answers):

    if len(answers) != 72 or any(response not in [1, 2, 3, 4, 5] for response in answers):
        return 'error answers count'

    sub_scales = {
        "Невинный младенец": [5, 13, 34, 49, 63, 65],
        "Сирота": [14, 22, 27, 30, 50, 71],
        "Воин": [6, 39, 40, 44, 57, 59],
        "Заботящийся": [7, 10, 15, 24, 55, 68],
        "Искатель": [33, 47, 51, 62, 70, 72],
        "Любящий": [12, 16, 17, 25, 29, 45],
        "Разрушитель": [2, 4, 21, 52, 61, 66],
        "Творец": [8, 19, 31, 60, 64, 69],
        "Правитель": [26, 32, 35, 38, 46, 67],
        "Маг": [3, 23, 37, 42, 48, 58],
        "Мудрец": [1, 18, 20, 36, 41, 56],
        "Дурак": [9, 11, 28, 43, 53, 54],

    }

    results = {}

    for scale, questions in sub_scales.items():
        score = sum(answers[q - 1] for q in questions)
        results[scale] = score

    results['Безопастность'] = results['Невинный младенец'] + results['Сирота']
    results['Индивидульность'] = results['Искатель'] + results['Любящий']
    results['Ответственность'] = results['Воин'] + results['Заботящийся']
    results['Аутентичность'] = results['Разрушитель'] + results['Творец']
    results['Сила'] = results['Правитель'] + results['Маг']
    results['Свобода'] = results['Мудрец'] + results['Дурак']

    results['Детство'] = max(results['Невинный младенец'], results['Сирота'])
    results['Юношество'] = max(results['Искатель'], results['Любящий'])
    results['Взрослый'] = max(results['Воин'], results['Заботящийся'])
    results['Средний возраст'] = max(results['Разрушитель'], results['Творец'])
    results['Зрелость'] = max(results['Правитель'], results['Маг'])
    results['Старость'] = max(results['Мудрец'], results['Дурак'])

    results['Эго'] = results['Безопастность'] + results['Ответственность']
    results['Душа'] = results['Индивидульность'] + results['Аутентичность']
    results['Самость'] = results['Сила'] + results['Свобода']

    return results


def holl(answers):

    if len(answers) != 30 or any(response not in [-3, -2, -1, 1, 2, 3] for response in answers):
        return 'error answers count'

    sub_scales = {
        "Эмоциональная осведомленность": [1, 2, 4, 17, 19, 25],
        "Управление своими эмоциями": [3, 7, 8, 10, 18, 30],
        "Самомотивация": [5, 6, 13, 14, 16, 22],
        "Эмпатия": [9, 11, 20, 21, 23, 28],
        "Распознавание эмоций других людей": [12, 15, 24, 26, 27, 29],
    }

    results = {}

    for scale, questions in sub_scales.items():
        score = sum(answers[q - 1] for q in questions)
        results[scale] = score

    results['Интеграционный уровень'] = sum(answers)

    return results


def SD(answers):

    new = [a if i % 2 == 1 else -a for i, a in enumerate(answers)]

    result ={
        '0': (new[0]+new[3]+new[6]+new[9])/4,
        'C': (new[1] + new[4] + new[7] + new[10]) / 4,
        'A': (new[2] + new[5] + new[8] + new[11]) / 4
    }

    return result

def LD(answers):

    new = [a if i % 2 == 1 else -a for i, a in enumerate(answers)]

    result ={
        '0': round((new[0]+new[3]+new[6]+new[9]+new[12]+new[15]+new[18])/ 7, 1),
        'C': round((new[1] + new[4] + new[7] + new[10]+new[13]+new[16]+new[19]) / 7, 1),
        'A': round((new[2] + new[5] + new[8] + new[11]+new[14]+new[17]+new[20]) / 7, 1)
    }

    return result



test_functions = {
    "plutchick": plutchick,
    'tomas': tomas,
    'CJO': CJO,
    'MIS': MIS,
    'leongard': leongard,
    'HMI': HMI,
    'holl': holl,
    'SD': SD,
    'LD': LD,
}

a = [1,4,3,1,5,4,1,4,3,5,2,3,4,1,2,5,5,4,5,5,2,1,4,3,4,4,1,2,5,2,1,5,5,2,5,4,5,4,5,5,4,4,1,3,4,4,4,5,2,1,4,4,3,3,3,2,4,3,3,4,4,1,4,5,2,1,5,2,3,5,4,4]
#print(HMI(a)) # корректно

a = [0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,1,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,1,0,0,1,1,]
#a = [1] * 88
print(leongard(a)) #хуйня

a = [1,1,1,0,1,0,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,1,0,0,0,0,1,1,1,1,1,0,1,0,0,1,1,0,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,0,0,0,1]
#print(MIS(a)) # охуенно

a = [0,1,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,]
#print(tomas(a)) #кайф

a = [6,2,4,4,1,4,2,6,7,2,6,4,1,1,1,1,2,3,1,4,]
#print(CJO(a))  # умение делать выбор - хуйня

a = [1,1,0,0,0,1,0,0,1,0,1,1,0,1,1,1,0,0,0,1,0,1,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1,0,1,0,0,]
#print(plutchick(a)) # охуенчик

a = [3,3,-3,2,3,-3,2,-3,2,-1,-2,1,1,1,1,3,1,-2,3,-2,-1,-2,-2,-2,3,1,2,1,1,-3]
#print(holl(a)) # охуенно

a = [2, -3, -3, -1, -3, -1, -3, 3, -3, 2, -3, 3]
#print(SD(a)) #кайф

a = [-2, -1, 1, 3, -2, -1, -3, -1, -2, 2, -2, -1, -3, -3, 3, 3, -2, 1,-2,2,-1]
#print(LD(a)) # кайф

##############################################################################################

a = [2,2,5,1,4,4,2,2,3,3,3,3,5,5,3,2,3,3,4,5,5,1,5,1,3,2,1,4,5,1,4,5,5,2,4,4,5,2,5,5,2,4,4,1,5,5,5,5,4,1,3,1,5,1,1,2,4,5,5,2,3,3,4,4,4,3,5,1,5,2,3,2]
#print(HMI(a)) #неверное подсчитано заботящийся

a = [0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,0,1,1,0,1,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,0,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,0,1,1,1,1,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,1,]
#print(leongard(a)) # хуйня

a = [1,0,0,1,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,1,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,1,0,0,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,]
#print(MIS(a)) # кайф

a = [0,0,0,0,0,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,0,1,0,0,1,]
#print(tomas(a)) # кайф

a = [-2,2,-2,2,-3,2,-3,-2,-2,2,-2,2,-3,1,-1,2,-2,2,-1,3,-2,]
#print(LD(a)) #кайф

a = [-2,3,-3,-1,2,-2,2,1,3,-1,1,3,3,2,1,-1,-2,2,3,3,3,1,3,1,3,3,3,2,2,-1,]
#print(holl(a)) #кайф

a = [5,3,5,5,2,2,1,6,6,3,3,5,2,1,2,5,5,3,4,3]
#print(CJO(a)) # не сходится локус контроля - Я

a = [0,1,1,1,1,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,1,0,1,0,1,0,0,0,1,1,1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,1,0,0,0,0,]
#print(plutchick(a)) # заебок


