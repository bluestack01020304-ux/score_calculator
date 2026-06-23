import dataManager as dataManager
import geminiManager as geminiManager
import mainUI as mainUI

import pandas as pd
import numpy as np
# def input_check(input_str: str):
#     isCheck = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

#     if input_str in isCheck:
#         return input_str
#     else:
#         return False

# menu_action = {
#     "1": work_김다진.add_student,
#     "2": work_김다진.show_students,
#     "3": work_김다진.search_student,
#     "4": work_김다진.calculate_total_average,
#     "5": work_김다진.grade_student,
#     "6": work_김다진.sort_by_total,
#     "7": work_김다진.filter_above_score,
#     "8": work_김다진.save_load_csv,
#     "9": work_김다진.summarize_statistics,
# }
#hello
def main():

    dataManager.initialize_data_manager() #초기화 안됌
    geminiManager.initialize_gemini_manager()

    # while(True):
    #     a = input("질문 입력: ")
    #     if a == "exit":
    #         break
        
    #     response = geminiManager.genarate_response(a)
    #     print(f"Gemini Response: {response}")
    
    mainUI.LogInUI()
    #success = dataManager.executeCommit("insert into students values ('10703', '홍길동', 85, 90, 95, 95, 88)")
    # students = [
        # {
        #     "name": "홍길동",
        #     "id": "10703",
        #     "subjects": {
        #         "korean": 85,
        #         "english": 90,
        #         "math": 95,
        #         "science": 95,
        #         "history": 88,
        #     }
        # },
        # {
        #     "name": "김철수",
        #     "id": "20705",
        #     "subjects": {
        #         "korean": 99,
        #         "english": 74,
        #         "math": 77,
        #         "science": 80,
        #         "history": 65,
        #     }
        # }
    # ]

    # while(True):
        
    #     work_임균정.display_menu()
    #     choice = input("입력: ")

    #     if input_check(choice) == False:
    #         print("잘못된 입력입니다.")
    #         continue
        
    #     print("---------------------------------------")
        
    #     if choice == "0":
    #         break

    #     action = menu_action.get(choice)

    #     if action:
    #         action()
    #     else:
    #         print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()