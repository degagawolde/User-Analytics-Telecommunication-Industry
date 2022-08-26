"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st


class MultipleApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func,data):

        self.apps.append({
            "title": title,
            "function": func,
            'data':data
        })

    def run(self):
        app = st.sidebar.radio(
            'Actions',
            self.apps,
            format_func=lambda app: app['title'])
        
        app['function'](app['data'])
