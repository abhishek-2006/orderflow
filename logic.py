from collections import deque
from storage import save_data, load_data, export_report

queue_list, served_list = load_data()

queue = deque(queue_list)
served_stack = served_list
next_id = len(queue) + len(served_stack) + 1

def add_order_logic(customer, items):
    global next_id
    if not customer:
        return
    order_str = f"#{next_id} — {customer}: {items}"
    queue.append(order_str)
    next_id += 1
    save_data(queue, served_stack)

def serve_order_logic():
    if queue:
        served_stack.append(queue.popleft())
        save_data(queue, served_stack)

def undo_served_logic():
    if served_stack:
        last = served_stack.pop()
        queue.appendleft(last)
        save_data(queue, served_stack)

def clear_all_logic():
    queue.clear()
    served_stack.clear()
    save_data(queue, served_stack)

def export_report_logic():
    export_report(queue, served_stack)

def get_queue():
    return list(queue)

def get_stack():
    return served_stack[::-1]
