from sway_utils.intention.app import App, sanitize_string, _input


task = sanitize_string(_input("What do you intend to do?", []))
mins = int(_input("For how many minutes?", ["25", "10", "5", "2"])) * 60
App(task, mins).run()
