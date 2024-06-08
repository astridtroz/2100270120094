import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from collections import deque

win_size = 10
limit = 0.5  # 500 milliseconds

class Number:
    def __init__(self):
        self.window = deque(maxlen=win_size)

    def fetch_numbers(self, number_type):
        url = f"http://20.244.56.144/test/{number_type}"
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json().get('numbers', [])
        except (requests.exceptions.RequestException, ValueError):
            return []

    def update_window(self, numbers):
        prev_state = list(self.window)
        for number in numbers:
            if number not in self.window:
                self.window.append(number)
        curr_state = list(self.window)
        avg = sum(self.window) / len(self.window) if self.window else 0
        return prev_state, curr_state, avg

number_service = Number()

class NumberAPIView(APIView):
    def get(self, request, numberid):
        if numberid not in ['primes', 'fibo', 'even', 'random']:
            return Response({"error": "Invalid number ID"}, status=status.HTTP_400_BAD_REQUEST)

        numbers = number_service.fetch_numbers(numberid)
        prev_state, curr_state, avg = number_service.update_window(numbers)

        return Response({
            "numbers": numbers,
            "windowPrevState": prev_state,
            "windowCurrState": curr_state,
            "avg": f"{avg:.2f}"
        }, status=status.HTTP_200_OK)
