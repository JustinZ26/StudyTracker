from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
# from kivy.graphics import Rectangle


class NavigationBox(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = 'horizontal'
        self.size_hint = (1, 0.1)
        self.add_widget(Button(text='Calendar', on_press=self.go_to_calendar))
        self.add_widget(Button(text='Home', on_press=self.go_to_home))
        self.add_widget(Button(text='Canvas', on_press=self.go_to_canvas))

    def go_to_calendar(self, instance): # TP
        self.screen_manager.current = 'calendar'

    def go_to_home(self, instance): # TP
        self.screen_manager.current = 'home'

    def go_to_canvas(self, instance): # TP
        self.screen_manager.current = 'canvas'


class StartPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Press any button to continue', on_press=self.go_to_home))
        self.add_widget(layout)

    def go_to_home(self, instance):
        self.manager.current = 'home'



class HomePage(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        layout = BoxLayout(orientation='vertical')

        # Heading for Upcoming Events
        layout.add_widget(Label(text='UPCOMING EVENTS', size_hint=(1, 0.1), font_size='20sp'))

        # Display Upcoming Events
        self.upcoming_events_label = Label(text='')
        layout.add_widget(self.upcoming_events_label)

        # Bottom Navigation Bar
        layout.add_widget(NavigationBox(screen_manager, size_hint=(1, 0.1)))

        self.add_widget(layout)

    def update_upcoming_events(self, events):
        # Clear previous text
        self.upcoming_events_label.text = ''

        if events:
            # Sort events by date
            sorted_events = sorted(events.items(), key=lambda x: x[0])
            
            for date, events_list in sorted_events:
                self.upcoming_events_label.text += f'\n\n{date}[Month][Year]\n'
                for event in events_list:
                    self.upcoming_events_label.text += f'{event}\n'
        else:
            self.upcoming_events_label.text = 'There is no upcoming event scheduled'

    def on_enter(self, *args):
        # Update upcoming events when the Home page is entered
        self.update_upcoming_events(self.screen_manager.get_screen('calendar').events)



class CalendarPage(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.events = {}
        self.date_selection = None

        layout = BoxLayout(orientation='vertical')

        # Top Section with Month/Year Label
        top_layout = BoxLayout(size_hint=(1, 0.1))
        self.month_year_label = Label(text='Month / Year')
        top_layout.add_widget(self.month_year_label)
        layout.add_widget(top_layout)

        # Middle Section with Date Buttons
        middle_layout = GridLayout(cols=7, spacing=5)
        for day in range(1, 32):
            date_button = Button(text=str(day), on_press=self.show_events_for_date)
            middle_layout.add_widget(date_button)
        layout.add_widget(middle_layout)

        # Space for Events and Add/Delete Event Button
        event_button_layout = BoxLayout(size_hint=(1, 0.5), orientation='horizontal')

        # Events Label
        self.events_label = Label(text='No Event scheduled for this day')
        event_button_layout.add_widget(self.events_label)

        # Add Event Button
        add_event_button = Button(text='Add Event', on_press=self.show_add_event_popup, size_hint=(0.2, 1))
        event_button_layout.add_widget(add_event_button)

        # Delete Event Button
        delete_event_button = Button(text='Delete Event', on_press=self.show_delete_event_popup, size_hint=(0.2, 1))
        event_button_layout.add_widget(delete_event_button)

        layout.add_widget(event_button_layout)

        # Bottom Navigation Bar
        layout.add_widget(NavigationBox(screen_manager))

        self.add_widget(layout)

    def add_event(self, selected_date, event_text, popup):
        if selected_date:
            if selected_date not in self.events:
                self.events[selected_date] = [event_text]
            else:
                self.events[selected_date].append(event_text)

        self.date_selection = selected_date
        self.show_events_for_date(Button(text=selected_date))

        # Clear user inputs
        popup.dismiss()
        self.clear_popup_inputs()

    def show_events_for_date(self, instance):
        selected_date = instance.text
        events_for_date = self.events.get(selected_date, [])
        
        if events_for_date:
            events_text = '\n'.join(events_for_date)
            self.events_label.text = f'Events on {selected_date} [Month][Year]:\n{events_text}'
        else:
            self.events_label.text = f'No events scheduled on {selected_date} [Month][Year]'

    def show_add_event_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical')

        # Date Selection Spinner
        date_selection_label = Label(text='Select Date:')
        self.date_selection_spinner = Spinner(text = 'Date', values=[str(day) for day in range(1, 32)])
        popup_content.add_widget(date_selection_label)
        popup_content.add_widget(self.date_selection_spinner)

        # Event Input
        self.event_input = TextInput(hint_text='Enter event here', multiline=True)
        popup_content.add_widget(Label(text='Enter Event:'))
        popup_content.add_widget(self.event_input)

        # Add Event Button
        add_button = Button(text='Add Event', on_press=lambda x: self.add_event(self.date_selection_spinner.text, self.event_input.text, popup))
        popup_content.add_widget(add_button)

        popup = Popup(title='Add Event', content=popup_content, size_hint=(None, None), size=(1000, 700))
        popup.open()

    def show_delete_event_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical')

        # Date Selection Spinner
        date_selection_label = Label(text='Select Date:')
        self.date_selection_spinner = Spinner(text='Date', values=[str(day) for day in range(1, 32)])
        popup_content.add_widget(date_selection_label)
        popup_content.add_widget(self.date_selection_spinner)

        # Delete Event Button
        delete_button = Button(text='Delete Event', on_press=self.delete_event)
        popup_content.add_widget(delete_button)

        popup = Popup(title='Delete Event', content=popup_content, size_hint=(None, None), size=(500, 300))
        popup.open()

    def delete_event(self, instance):
        selected_date = self.date_selection_spinner.text
        if selected_date and selected_date in self.events:
            del self.events[selected_date]

        self.date_selection = selected_date
        self.show_events_for_date(Button(text=selected_date))

        # Clear user inputs
        self.clear_popup_inputs()

    def clear_popup_inputs(self):
        self.date_selection_spinner.text = 'Select Date'

    def get_selected_date(self):
        return self.month_year_label.text.split('/')[1]


class MyPaintWidget(Widget):
    current_color = (1, 1, 1, 1)  # Default color (White)

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.current_color)
            d = 5
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]



class CanvasPage(Screen):
    colors = {
            'white': (1, 1, 1, 1),
            'red': (1, 0, 0, 1), 
            'yellow': (1, 1, 0, 1), 
            'green': (0, 1, 0, 1), 
            'blue': (0, 0, 1, 1)
    }

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Canvas for drawing
        canvas_layout = BoxLayout(size_hint=(1, 0.9))
        self.painter = MyPaintWidget()
        canvas_layout.add_widget(self.painter)

        # Buttons for selecting colors
        color_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        clear_button = Button(text='Clear', size_hint=(None, None), size=(100, 100))
        clear_button.bind(on_release=self.clear_canvas)
        color_layout.add_widget(clear_button)

        for color, rgb_values in self.colors.items():
            color_button = Button(size_hint=(None, None), size=(100, 100), background_color=rgb_values)
            color_button.bind(on_release=lambda btn, c=color: self.set_brush_color(c))
            color_layout.add_widget(color_button)

        canvas_layout.add_widget(color_layout)

        layout.add_widget(canvas_layout)

        # Bottom Navigation Bar with increased size
        navigation_layout = NavigationBox(screen_manager, size_hint=(1, 0.1))
        layout.add_widget(navigation_layout)

        self.add_widget(layout)

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

    def set_brush_color(self, color):
        # Set the color of the brush
        self.painter.current_color = self.colors[color]



class StudyTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartPage(name='start'))
        sm.add_widget(HomePage(name='home', screen_manager=sm))
        sm.add_widget(CalendarPage(name='calendar', screen_manager=sm))
        sm.add_widget(CanvasPage(name='canvas', screen_manager=sm))
        return sm

if __name__ == '__main__':
    StudyTrackerApp().run()
