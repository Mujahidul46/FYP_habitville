import { defineStore } from 'pinia';

export const useToDoStore = defineStore('todo', {
  state: () => ({
    csrfToken: '',
    newTodo: {
      id: null,
      title: '',
      notes: ''
    },
    todos: [],
    accomplishedTodos: [],
    currentView: 'todos',
    showForm: false,
    editingTodo: null,
    showDeleteConfirm: false,
    toDeleteTodo: null,
  }),
  getters: {
  },
  actions: {
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
      async fetchToDos() {
        try {
          const response = await fetch("http://localhost:8000/list-todo/", {
            credentials: 'include'
          });
          if (response.ok) {
            const fetchedTodos = await response.json();
            this.todos = fetchedTodos.filter(todo => !todo.completed);
          } else {
            console.error('Failed to fetch to-dos:', await response.text());
          }
        } catch (error) {
          console.error('Error fetching to-dos:', error);
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
            if (!createdTodo.completed) {
              this.todos.push(createdTodo);
            }
            this.resetForm(); 
            this.showForm = false;
          } else {
            console.error('Failed to create to-do:', await response.text());
          }
        } catch (error) {
          console.error('Error creating to-do:', error);
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
      async markAsCompleted(todo) {
        try {
          const response = await fetch(`http://localhost:8000/mark-completed/${todo.id}/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken,
            },
            body: JSON.stringify({ completed: true }),
            credentials: 'include',
          });
    
          if (response.ok) {
            this.todos = this.todos.filter(t => t.id !== todo.id);
            await this.fetchAccomplishedToDos();
          } else {
            console.error('Failed to mark to-do as completed:', await response.text());
          }
        } catch (error) {
          console.error('Error marking to-do as completed:', error);
        }
      },
      async fetchAccomplishedToDos() {
        try {
          const response = await fetch(`http://localhost:8000/list-completed/`, {
            credentials: 'include',
          });
          if (response.ok) {
            this.accomplishedTodos = await response.json();
          } else {
            console.error('Failed to fetch accomplished to-dos:', await response.text());
          }
        } catch (error) {
          console.error('Error fetching accomplished to-dos:', error);
        }
      },
      toggleView(view) {
        this.currentView = view;
        if (view === 'accomplished') {
          this.fetchAccomplishedToDos();
        }
      },
      editTodo(todo) {
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
                  const index = this.todos.findIndex(todo => todo.id === this.newTodo.id);
                  if (index !== -1) {
                    this.todos[index] = { ...this.todos[index], ...todoData };
                  }
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
      async deleteToDo() {
        if (!this.toDeleteTodo) return;
        try {
          const response = await fetch(`http://localhost:8000/delete-todo/${this.toDeleteTodo.id}/`, {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': this.csrfToken,
            },
            credentials: 'include',
          });
    
          if (response.ok) {
            this.todos = this.todos.filter(todo => todo.id !== this.toDeleteTodo.id);
            this.resetForm(); 
            this.showForm = false;
            this.showDeleteConfirm = false; 
            this.toDeleteTodo = null; 
          } else {
            console.error('Failed to delete to-do:', await response.text());
          }
        } catch (error) {
          console.error('Error deleting to-do:', error);
        }
      },
    
      confirmDelete(todo) {
        this.toDeleteTodo = todo;
        this.showDeleteConfirm = true; 
      },
    
      cancelDelete() {
        this.showDeleteConfirm = false; 
        this.toDeleteTodo = null; 
      },
  },
});
