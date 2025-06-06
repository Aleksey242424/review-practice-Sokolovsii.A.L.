def factorial(n):
    result = 1
    for i in range(1, n+1):  
        result *= i
    return result

# Тест: 
print(factorial(5))  # Ожидается 120, выводит 24




def check_password(password):
  if password == "qwerty":
    return "Your password qwerty"
  if len(password) < 8:                  
    return "Слишком короткий!"          # Step Over
  elif not any(char.isdigit() for char in password):
    return "Нет цифр!"                 
  else:
    return "Пароль надёжен!" 

print(check_password("qwerty"))  # Должно вернуть "Слишком короткий!"



def calculate_sum(arr):
    total = 0
    for i in range(0, len(arr)):  # Ошибка: выход за границы массива
        total += arr[i]
    return total

# Тест: 
numbers = [10, 20, 30]
print(calculate_sum(numbers))  # Ожидается 60, но возникает IndexError
