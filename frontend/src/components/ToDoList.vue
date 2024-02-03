<template>
    <div class="habit-tracker">
      <div class="todo-list-container">
        <button
          class="view-toggle"
          :class="{ active: todoStore.currentView === 'todos' }"
          @click="todoStore.toggleView('todos')"
        >To Do's</button>
  
        <button
          class="view-toggle"
          :class="{ active: todoStore.currentView === 'accomplished' }"
          @click="todoStore.toggleView('accomplished')"
        >Accomplished</button>
        <button class="add-todo-btn" @click="todoStore.toggleForm">Add a To Do</button>
  
        <div v-if="todoStore.currentView === 'todos' && !todoStore.todos.length" class="empty-todo-list">
          <div class="empty-todo-content">
            <h3 class="emptyTitle">You have no To Do's</h3>
            <p>These are one-off tasks. For example, "book an appointment" or "send an email to Alice".</p>
          </div>
        </div>
  
        <ul v-else-if="todoStore.currentView === 'todos'">
          <li v-for="todo in todoStore.todos" :key="todo.id" class="todo-item">
            <div class="todo-checkbox" @click.stop="todoStore.markAsCompleted(todo)">
              <i class="far" :class="{ 'fa-square': !todo.completed, 'fa-check-square': todo.completed }"></i>
            </div>
            <div class="todo-content" @click="todoStore.editTodo(todo)">
              <h3>{{ todo.title }}</h3>
              <p>{{ todo.notes }}</p>
            </div>
            <i class="fas fa-trash delete-todo-btn" @click.stop="todoStore.confirmDelete(todo)"></i>
          </li>
        </ul>
  
        <ul v-if="todoStore.currentView === 'accomplished'" class="accomplished">
          <li v-if="!todoStore.accomplishedTodos.length" class="empty-todo-list">
            <div class="empty-todo-content">
              <h3 class="emptyTitle">Your accomplished tasks will appear here!</h3>
              <p>Complete tasks to see them in this list.</p>
            </div>
          </li>
          <li v-for="todo in todoStore.sortedAccomplishedTodos" :key="todo.id" class="todo-item">
            <div class="todo-content">
              <h3>{{ todo.title }}</h3>
              <p>{{ todo.notes }}</p>
              <small>{{ formatDate(todo.completed_at) }}</small>
            </div>
          </li>
        </ul>
      </div>
  
      <div v-if="todoStore.showForm" class="modal-backdrop">
        <div class="modal-content">
          <h2 class="form-title">{{ todoStore.editingTodo ? 'Edit To Do' : 'Create To Do' }}</h2>
          <form @submit.prevent="todoStore.handleSubmit">
            <label for="titleInput">Title<span class="required-asterisk">*</span></label>
            <input id="titleInput" v-model="todoStore.newTodo.title" placeholder="Add a title" required>
            <label for="notesInput">Notes</label>
            <textarea id="notesInput" v-model="todoStore.newTodo.notes" placeholder="Add notes"></textarea>
            <div class="modal-footer">
              <button v-if="todoStore.editingTodo" type="button" class="delete-edit-todo-btn" @click="todoStore.confirmDelete(todoStore.editingTodo)">
                Delete
              </button>
              <button type="button" @click="todoStore.toggleForm">Cancel</button>
              <button type="submit">{{ todoStore.editingTodo ? 'Update' : 'Create' }}</button>
            </div>
          </form>
        </div>
      </div>
  
      <div v-if="todoStore.showDeleteConfirm" class="modal-backdrop">
        <div class="modal-content">
          <h2 class="form-title">Are you sure you want to delete this To Do item?</h2>
          <div class="modal-footer">
            <button type="button" @click="todoStore.cancelDelete">Cancel</button>
            <button type="button" @click="todoStore.deleteToDo">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import { toRefs } from 'vue';
import { useToDoStore } from '@/stores/useToDoStore';
import { formatDate } from '@/utils/dateUtils';

export default {
  name: 'ToDoList',
  setup() {
    const todoStore = useToDoStore();
    const {
      csrfToken,
      newTodo,
      todos,
      accomplishedTodos,
      currentView,
      toDeleteTodo,
    } = toRefs(todoStore);

    return {
      todoStore,
      csrfToken,
      newTodo,
      todos,
      accomplishedTodos,
      currentView,
      toDeleteTodo,
      formatDate,
    };
  },
};
</script>

<style scoped>
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
    background-color: #e0e0e0;
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
      transition: border-color 0.3s ease;
      cursor: pointer;
      padding: 10px;
      border: 2px solid transparent;
      border-radius: 10px;
      display: flex;
      align-items: center; 
    }

    .todo-item:hover {
        border-color: #faa404;
    }

    .todo-content {
      flex-grow: 1;
      padding: 5px;
      text-align: left;
    }

    .todo-content h3 {
      word-break: break-all;
      margin: 0;
      font-size: 18px; 
    }

    .todo-content p {
      word-break: break-all;
      margin: 0;
      font-size: 14px; 
    }
    .delete-todo-btn {
    visibility: hidden; 
    color: #f44336; 
    cursor: pointer;
    flex-shrink: 0;
    }

    .todo-item:hover .delete-todo-btn {
    visibility: visible; 
    }

    .modal-footer .delete-edit-todo-btn {
    padding: 0.5em;
    background-color: #f44336; 
    color: white;
    border: none;
    cursor: pointer;
    }

    .todo-checkbox {
      margin-right: 10px; 
      flex-shrink: 0; 
    }

    .view-toggle {
      margin-right: 10px; 
    }

    .empty-todo-list {
      text-align: center;
      margin-top: 10em; 
      color: #a8a4a4;
      background-color: #e0e0e0;
    }

    .empty-todo-content h3 {
      margin-bottom: 0.5em;
    }

    .empty-todo-content p {
      font-style: italic;
    }

    .view-toggle {
      margin-right: 10px;
      background-color: #e0e0e0; 
    }

    .view-toggle.active {
      background-color: #9540df; 
      color: white; 
    }

    .emptyTitle {
      font-size: 1.3em;
    }

    .accomplished .todo-item {
      cursor: default;
    }

    .modal-footer button[type="submit"],
    .modal-footer button[type="button"] {
      cursor: pointer; 
    }
</style>
