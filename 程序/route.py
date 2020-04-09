from app import *
from app.views import *

index = Route_map("/", login, ["POST", "GET"])
maps = [
    Route_map("/index", home, ["POST", "GET"]),
    Route_map("/logout", logout, ["POST", "GET"]),
    Route_map("/filter", filter, ["POST", "GET"]),
    Route_map("/show_clean_content", show_clean_content, ["POST", "GET"]),
    Route_map("/show_symptom_content", show_symptom_content, ["POST", "GET"]),
    Route_map("/show_tongue_content", show_tongue_content, ["POST", "GET"]),
    Route_map("/show_pulse_content", show_pulse_content, ["POST", "GET"]),
    Route_map("/show_syndrome_content", show_syndrome_content, ["POST", "GET"]),
    Route_map("/show_input_content", show_input_content, ["POST", "GET"]),
    Route_map("/show_diagnose_content", show_diagnose_content, ["POST", "GET"]),
    Route_map("/show_result_content", show_result_content, ["POST", "GET"]),
    Route_map("/show_algorithm_content", show_algorithm_content, ["POST", "GET"]),
    Route_map("/show_display_content", show_display_content, ["POST", "GET"]),
    Route_map("/show_train_content", show_train_content, ["POST", "GET"]),
    Route_map("/search_pulse", search_pulse, ["POST", "GET"]),
    Route_map("/add_pulse", add_pulse, ["POST", "GET"]),
    Route_map("/update_pulse", update_pulse, ["POST", "GET"]),
    Route_map("/delete_pulse", delete_pulse, ["POST", "GET"]),
    Route_map("/search_tongue", search_tongue, ["POST", "GET"]),
    Route_map("/add_tongue", add_tongue, ["POST", "GET"]),
    Route_map("/update_tongue", update_tongue, ["POST", "GET"]),
    Route_map("/delete_tongue", delete_tongue, ["POST", "GET"]),
    Route_map("/search_symptom", search_symptom, ["POST", "GET"]),
    Route_map("/add_symptom", add_symptom, ["POST", "GET"]),
    Route_map("/update_symptom", update_symptom, ["POST", "GET"]),
    Route_map("/delete_symptom", delete_symptom, ["POST", "GET"]),
    Route_map("/search_syndrome", search_syndrome, ["POST", "GET"]),
    Route_map("/add_syndrome", add_syndrome, ["POST", "GET"]),
    Route_map("/update_syndrome", update_syndrome, ["POST", "GET"]),
    Route_map("/delete_syndrome", delete_syndrome, ["POST", "GET"]),
    Route_map("/update_clean", update_clean, ["POST", "GET"]),
    Route_map("/delete_clean", delete_clean, ["POST", "GET"]),
    Route_map("/form_upload", form_upload, ["POST", "GET"]),
    Route_map("/text_upload", text_upload, ["POST", "GET"]),
    Route_map("/excel_upload", excel_upload, ["POST", "GET"]),
    Route_map("/database_upload", database_upload, ["POST", "GET"]),
    Route_map("/get_graph", get_graph, ["POST", "GET"]),
    Route_map("/add_train", add_train, ["POST", "GET"]),
    Route_map("/update_train", update_train, ["POST", "GET"]),
    Route_map("/delete_train", delete_train, ["POST", "GET"]),
    Route_map("/get_data", get_data, ["POST", "GET"]),
    Route_map("/predict", predict, ["POST", "GET"]),
]


def load_user(token):
    key = current_app.config.get("SECRET_KEY", "beornut@gmail.com")
    user = handler.load_token(key, token)
    return user


def unauthorized():
    return redirect(url_for('login', tag='error'))
