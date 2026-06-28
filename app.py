from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Task 2 - Parse the incoming JSON body
    data = request.get_json()

    # Task 3 - Validate that 'title' exists in the payload
    if not data or "title" not in data:
        return jsonify({"error": "A 'title' field is required"}), 400

    # Task 4 - Generate a new ID, create the Event, append, and return
    new_id = max(event.id for event in events) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Task 2 - Parse the incoming JSON body
    data = request.get_json()

    # Task 3 - Loop through events to find the matching one
    for event in events:
        if event.id == event_id:
            # Validate that 'title' is present in the payload
            if not data or "title" not in data:
                return jsonify({"error": "A 'title' field is required"}), 400

            # Update the title (partial update — PATCH only touches what's sent)
            event.title = data["title"]

            # Task 4 - Return the updated event
            return jsonify(event.to_dict()), 200

    # No matching event was found
    return jsonify({"error": f"Event with id {event_id} not found"}), 404


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Task 2 - Declare global so we can reassign the list
    global events

    # Task 3 - Check if the event exists before attempting deletion
    event_to_delete = next((event for event in events if event.id == event_id), None)

    if event_to_delete is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    # Filter the event out of the list
    events = [event for event in events if event.id != event_id]

    # Task 4 - Return 204 No Content (no body on successful delete)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)