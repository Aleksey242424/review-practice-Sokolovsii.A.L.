"""
calculate_positive_average принимает список из чисел,возвращает число 
(среднее арифметическое значение)
"""
def calculate_positive_average(numbers:arr[int])->int:
    """
    Вычисляет среднее арифметическое положительных элементов в списке `numbers`.
    Возвращает 0, если положительных элементов нет.
    """
    total = 0
    count = 0
    for num in numbers:
	"""
	допустим нам будет дан список ввиде [1,2,3,4],
	первая итерация:
	total = 1
	count = 1
	вторая итерация:
	total = 3
	count = 2
	третяя итерация:
	total = 6
	count = 3
	четвёртая итерация:
	total = 10
	count = 4
	"""
        if num > 0:
            total += num
            count += 1
    if count > 0:
        average = total / count  # Строка A
    else:
        average = 0
    return average
