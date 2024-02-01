<template>
    <div class="habit-tracker">
        <h1>This is your habit tracker!</h1>
        <div class="todo-list-container">
            <h2>Your To Dos</h2>
            <button class="add-todo-btn" @click="toggleForm">Add a To Do</button>
            <ul>
                <li v-for="todo in todos" :key="todo.id" class="todo-item" @click="editTodo(todo)">
                    <div class="todo-content">
                        <h3>{{ todo.title }}</h3>
                        <p>{{ todo.notes }}</p>
                    </div>
                </li>
            </ul>
        </div>
        <div v-if="showForm" class="modal-backdrop">
            <div class="modal-content" @click.stop>
                <h2 class="form-title">{{ editingTodo ? 'Edit To Do' : 'Create To Do' }}</h2>
                <form @submit.prevent="handleSubmit">
                    <label for="titleInput">Title<span class="required-asterisk">*</span></label>
                    <input id="titleInput" v-model="newTodo.title" placeholder="Add a title" required>
                    <label for="notesInput">Notes</label>
                    <textarea id="notesInput" v-model="newTodo.notes" placeholder="Add notes"></textarea>
                    <div class="modal-footer">
                        <button type="button" @click="toggleForm">Cancel</button>
                        <button type="submit">{{ editingTodo ? 'Update' : 'Create' }}</button>
                    </div>
                </form>
            </div>
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
        id: null, 
        title: '',
        notes: ''
      },
      todos: [],
      showForm: false,
      editingTodo: null, 
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
            this.showForm = false;
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
        },
        toggleForm() {
            this.showForm = !this.showForm;
            if (!this.showForm) {
                this.editingTodo = null; 
                this.resetForm();
      }
    },
    resetForm() {
        this.newTodo = { id: null, title: '', notes: '' };
        this.editingTodo = null;
    },
    async editTodo(todo) {
      this.newTodo.id = todo.id;
      this.newTodo.title = todo.title;
      this.newTodo.notes = todo.notes;
      this.editingTodo = todo;
      this.showForm = true;
    },
    async handleSubmit() {
        if (this.editingTodo) {
            await this.updateToDo(); 
        } else {
            await this.createToDo(); 
        }
        this.resetForm(); 
        this.showForm = false; 
    },
    async updateToDo() {
        console.log("Updating todo with data:", this.newTodo);
        try {
            const url = this.newTodo.id 
                ? `http://localhost:8000/update-todo/${this.newTodo.id}/` 
                : `http://localhost:8000/create-todo/`;
            const method = this.newTodo.id ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                },
                body: JSON.stringify({
                    title: this.newTodo.title,
                    notes: this.newTodo.notes
                }),
                credentials: 'include',
            });

            if (response.ok) {
                const todoData = await response.json();

                if (this.newTodo.id) {
                    const updatedTodos = this.todos.map(todo =>
                        todo.id === this.newTodo.id ? { ...todo, ...todoData } : todo
                    );
                    this.todos = updatedTodos;
                } else {
                    this.todos.push(todoData);
                }

                this.resetForm();
                this.showForm = false;
            } else {
                console.error('Failed to update to-do:', await response.text());
            }
        } catch (error) {
            console.error('Error updating to-do:', error);
        }
    },
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

    .form-title {
        text-align: center;
        margin-top: 0; 
        margin-bottom: 1rem; 
    }

    .habit-tracker input,
    .habit-tracker textarea {
    margin-bottom: 0.5em;
    padding: 0.5em;
    border: 1px solid #ccc;
    width: 100%; 
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
    overflow: hidden; 
    }

    .habit-tracker h3,
    .habit-tracker p {
    word-wrap: break-word; 
    overflow-wrap: break-word; 
    margin: 0; 
    }

    .todo-list-container {
    width: 500px;
    height: 600px;
    overflow: auto;
    border: 2px solid #4CAF50;
    margin: auto;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    padding: 1em;
    background-color: #ffffff;
    position: relative;
    }

    .add-todo-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    cursor: pointer;
    padding: 0.5em;
    background-color: #4CAF50;
    color: white;
    border: none;
    }

    .todo-item {
        transition: border-color 0.05s ease; 
        cursor: pointer; 
        padding: 10px; 
        border: 2px solid transparent; 
        border-radius: 10px; 
    }

    .todo-item:hover {
        border-color: #faa404; 
    }

    .todo-content h3, 
    .todo-content p {
        margin: 0; 
        padding: 5px; 
    }

</style>

