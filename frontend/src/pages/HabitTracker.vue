<template>
    <div class="habit-tracker">
      <h1>This is your habit tracker!</h1>
  
      <div>
        <h2>Add a new To Do</h2>
        <form @submit.prevent="createToDo">
          <input v-model="newTodo.title" placeholder="Title" required>
          <textarea v-model="newTodo.notes" placeholder="Notes"></textarea>
          <button type="submit">Create</button>
        </form>
      </div>
  
      <div>
        <h2>Your To Dos</h2>
        <ul>
          <li v-for="todo in todos" :key="todo.id">
            <h3>{{ todo.title }}</h3>
            <p>{{ todo.notes }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HabitTracker',
    data() {
      return {
        csrfToken: '', 
        newTodo: {
          title: '',
          notes: ''
        },
        todos: []
      };
    },
    methods: {
        async fetchCSRFToken() {
            try {
                const response = await fetch("http://localhost:8000/csrf/", {
                credentials: 'include'
                });
                const data = await response.json();
                this.csrfToken = data.csrftoken; 
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
            }
            },
        async createToDo() {
            console.log("Creating new todo with data:", this.newTodo);
            try {
                const response = await fetch("http://localhost:8000/create-todo/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                },
                body: JSON.stringify(this.newTodo),
                credentials: 'include',
                });
                if (response.ok) {
                const createdTodo = await response.json();
                this.todos.push(createdTodo);
                this.newTodo.title = '';
                this.newTodo.notes = '';
                
                this.fetchToDos();
                } else {
                console.error('Failed to create to-do:', await response.text());
                }
            } catch (error) {
                console.error('Error creating to-do:', error);
            }
            },
      async fetchToDos() {
        try {
          const response = await fetch("http://localhost:8000/list-todo/", {
            credentials: 'include' 
          });
          if (response.ok) {
            this.todos = await response.json();
          } else {
            console.error('Failed to fetch to-dos:', await response.text());
          }
        } catch (error) {
          console.error('Error fetching to-dos:', error);
        }
      }
    },
    created() {
      this.fetchCSRFToken(); 
      this.fetchToDos();
    }
  };
  </script>
  
  
  <style>
  .habit-tracker form {
    margin-bottom: 1em;
  }
  
  .habit-tracker input, .habit-tracker textarea {
    margin-bottom: 0.5em;
    padding: 0.5em;
    border: 1px solid #ccc;
  }
  
  .habit-tracker button {
    padding: 0.5em;
    background-color: #4CAF50;
    color: white;
    border: none;
  }
  
  .habit-tracker ul {
    list-style: none;
    padding: 0;
  }
  
  .habit-tracker li {
    margin-bottom: 1em;
    background-color: #f9f9f9;
    padding: 1em;
    border-radius: 5px;
  }
  
  .habit-tracker h3 {
    margin-top: 0;
  }
  </style>
  