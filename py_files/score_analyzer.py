
def percentage(this_test_marks,previous_test_marks,this_test_max_marks,previous_test_max_marks):

    this_test_percentage=int((this_test_marks/this_test_max_marks)*100)
    previous_test_percentage=int((previous_test_marks/previous_test_max_marks)*100)
    performance_factor=float((this_test_percentage - previous_test_percentage)/100)
    
    container=[this_test_percentage,previous_test_percentage,performance_factor]

    return container
