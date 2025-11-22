# Job Search API - Frontend Integration Guide

Документация для фронтенд разработчиков по интеграции с Job Search API.

## Базовый URL

```
http://127.0.0.1:8000
```

## Аутентификация

API использует JWT (JSON Web Tokens) для аутентификации. После успешного входа вы получите два токена:
- **access** - используется для авторизованных запросов (действителен 15 минут)
- **refresh** - используется для обновления access токена (действителен 1 день)

### Формат заголовка авторизации

```javascript
Authorization: Bearer <access_token>
```

---

## 1. Регистрация

**POST** `/auth/register/`

Регистрация нового пользователя.

### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/auth/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'employer1',
    email: 'employer@example.com',
    password: 'password123',
    confirm_password: 'password123',
    role: 'employer' // или 'seeker'
  })
});

const data = await response.json();
```

### Ответ (201 Created)

```json
{
  "id": 1,
  "username": "employer1",
  "email": "employer@example.com",
  "first_name": "",
  "last_name": "",
  "role": "employer"
}
```

### Ошибки

- `400 Bad Request` - если пароли не совпадают или данные невалидны
- `400 Bad Request` - если username уже существует

---

## 2. Вход (Login)

**POST** `/auth/login/`

Вход в систему и получение JWT токенов.

### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'employer1',
    password: 'password123'
  })
});

const data = await response.json();
// Сохраните токены
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
```

### Ответ (200 OK)

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Ошибки

- `400 Bad Request` - неверные учетные данные

---

## 3. Обновление токена

**POST** `/auth/refresh/`

Обновление access токена с помощью refresh токена.

### Запрос

```javascript
const refreshToken = localStorage.getItem('refresh_token');

const response = await fetch('http://127.0.0.1:8000/auth/refresh/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    token: refreshToken
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
```

### Ответ (200 OK)

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 4. Выход (Logout)

**POST** `/auth/logout/`

Выход из системы (добавляет refresh токен в blacklist).

### Запрос

```javascript
const refreshToken = localStorage.getItem('refresh_token');

await fetch('http://127.0.0.1:8000/auth/logout/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    token: refreshToken
  })
});

// Удалите токены из localStorage
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
```

### Ответ (205 Reset Content)

```json
{
  "detail": "User logged out!"
}
```

---

## 5. Вакансии

### 5.1. Получить список вакансий

**GET** `/api/vacancies/`

Получить список всех вакансий.

#### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/api/vacancies/');
const data = await response.json();
```

#### Ответ (200 OK)

```json
[
  {
    "id": 1,
    "title": "Python Developer",
    "company": {
      "id": 1,
      "name": "Tech Company",
      "logo": "/media/company_logos/logo.png",
      "description": "Описание компании",
      "website": "https://example.com"
    },
    "location": "Душанбе",
    "description": "Описание вакансии",
    "responsibilities": "Обязанности",
    "requirements": "Требования",
    "salary_from": "5000.00",
    "salary_to": "8000.00",
    "currency": "TJS",
    "show_salary": true,
    "employment_type": "full_time",
    "work_format": "remote",
    "experience_required": "1_3",
    "is_active": true,
    "views": 42,
    "created_at": "2025-11-22T12:00:00Z",
    "updated_at": "2025-11-22T12:00:00Z",
    "author": "employer1",
    "salary_display": "5000.00 – 8000.00 TJS"
  }
]
```

### 5.2. Поиск вакансий по названию

**GET** `/api/vacancies/?t=python`

#### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/api/vacancies/?t=python');
const data = await response.json();
```

### 5.3. Фильтр вакансий по дате

**GET** `/api/vacancies/?d=2025-11-21`

#### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/api/vacancies/?d=2025-11-21');
const data = await response.json();
```

### 5.4. Получить детали вакансии

**GET** `/api/vacancies/<id>/`

Примечание: При каждом запросе счетчик просмотров автоматически увеличивается.

#### Запрос

```javascript
const vacancyId = 1;
const response = await fetch(`http://127.0.0.1:8000/api/vacancies/${vacancyId}/`);
const data = await response.json();
```

### 5.5. Создать вакансию

**POST** `/api/vacancies/`

⚠️ **Только для пользователей с ролью `employer`**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');

const response = await fetch('http://127.0.0.1:8000/api/vacancies/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    title: "Python Developer",
    company_id: 1,
    location: "Душанбе",
    description: "Описание вакансии",
    responsibilities: "Обязанности",
    requirements: "Требования",
    salary_from: 5000,
    salary_to: 8000,
    currency: "TJS",
    show_salary: true,
    employment_type: "full_time", // full_time, part_time, contract, internship, fifo, volunteer
    work_format: "remote", // on_site, remote, hybrid, shift
    experience_required: "1_3" // no_exp, 1_3, 3_6, 6_plus
  })
});

const data = await response.json();
```

#### Ответ (201 Created)

Возвращает созданную вакансию.

#### Ошибки

- `403 Forbidden` - если пользователь не является employer
- `401 Unauthorized` - если токен недействителен

### 5.6. Обновить вакансию

**PUT** `/api/vacancies/<id>/`

⚠️ **Только автор вакансии может её редактировать**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');
const vacancyId = 1;

const response = await fetch(`http://127.0.0.1:8000/api/vacancies/${vacancyId}/`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    title: "Updated Title",
    company_id: 1,
    location: "Душанбе",
    // ... остальные поля
  })
});

const data = await response.json();
```

### 5.7. Удалить вакансию

**DELETE** `/api/vacancies/<id>/`

⚠️ **Только автор вакансии может её удалить**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');
const vacancyId = 1;

const response = await fetch(`http://127.0.0.1:8000/api/vacancies/${vacancyId}/`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

// 204 No Content при успехе
```

---

## 6. Резюме

### 6.1. Получить список резюме

**GET** `/api/resumes/`

Возвращает только активные резюме.

#### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/api/resumes/');
const data = await response.json();
```

#### Ответ (200 OK)

```json
[
  {
    "id": 1,
    "user": "seeker1",
    "full_name": "Иван Иванов",
    "desired_position": "Python Developer",
    "location": "Душанбе",
    "phone": "+992901234567",
    "email": "ivan@example.com",
    "salary_expectation": "6000.00",
    "experience_years": 2,
    "about": "О себе...",
    "skills": [
      {"id": 1, "name": "Python"},
      {"id": 2, "name": "Django"}
    ],
    "is_active": true,
    "created_at": "2025-11-22T12:00:00Z",
    "updated_at": "2025-11-22T12:00:00Z"
  }
]
```

### 6.2. Поиск резюме по навыку

**GET** `/api/resumes/?skill=Django`

#### Запрос

```javascript
const response = await fetch('http://127.0.0.1:8000/api/resumes/?skill=Django');
const data = await response.json();
```

### 6.3. Создать резюме

**POST** `/api/resumes/`

⚠️ **Только для пользователей с ролью `seeker`**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');

const response = await fetch('http://127.0.0.1:8000/api/resumes/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    full_name: "Иван Иванов",
    desired_position: "Python Developer",
    location: "Душанбе",
    phone: "+992901234567",
    email: "ivan@example.com",
    salary_expectation: 6000,
    experience_years: 2,
    about: "О себе...",
    skill_ids: [1, 2, 3], // ID навыков
    is_active: true
  })
});

const data = await response.json();
```

### 6.4. Обновить резюме

**PUT** `/api/resumes/<id>/`

⚠️ **Только владелец резюме может его редактировать**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');
const resumeId = 1;

const response = await fetch(`http://127.0.0.1:8000/api/resumes/${resumeId}/`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    full_name: "Иван Иванов",
    // ... остальные поля
  })
});

const data = await response.json();
```

### 6.5. Удалить резюме

**DELETE** `/api/resumes/<id>/`

⚠️ **Только владелец резюме может его удалить**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');
const resumeId = 1;

const response = await fetch(`http://127.0.0.1:8000/api/resumes/${resumeId}/`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

---

## 7. Отклики на вакансии

### 7.1. Откликнуться на вакансию

**POST** `/api/vacancies/<vacancy_id>/apply/`

⚠️ **Только для пользователей с ролью `seeker`**

⚠️ **Нельзя откликнуться дважды на одну вакансию**

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');
const vacancyId = 1;

const response = await fetch(`http://127.0.0.1:8000/api/vacancies/${vacancyId}/apply/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    cover_letter: "Я заинтересован в этой вакансии...",
    resume_id: 1 // опционально
  })
});

const data = await response.json();
```

#### Ответ (201 Created)

```json
{
  "id": 1,
  "applicant": "seeker1",
  "vacancy": "Python Developer в Tech Company",
  "resume": {
    "id": 1,
    "full_name": "Иван Иванов",
    // ... остальные поля резюме
  },
  "cover_letter": "Я заинтересован в этой вакансии...",
  "status": "pending",
  "applied_at": "2025-11-22T12:00:00Z",
  "updated_at": "2025-11-22T12:00:00Z"
}
```

#### Ошибки

- `403 Forbidden` - если пользователь не является seeker
- `400 Bad Request` - если уже есть отклик на эту вакансию

---

## 8. Избранное

### 8.1. Добавить/убрать из избранного

**POST** `/api/vacancies/<vacancy_id>/favorite/`

⚠️ **Только для пользователей с ролью `seeker`**

Это toggle-эндпоинт: если вакансия уже в избранном, она будет удалена, если нет - добавлена.

#### Запрос

```javascript
const accessToken = localStorage.getItem('access_token');
const vacancyId = 1;

const response = await fetch(`http://127.0.0.1:8000/api/vacancies/${vacancyId}/favorite/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const data = await response.json();
```

#### Ответ (200 OK или 201 Created)

```json
{
  "message": "Added to favorites"
}
```

или

```json
{
  "message": "Removed from favorites"
}
```

---

## Примеры использования

### Утилита для работы с API

```javascript
class JobSearchAPI {
  constructor(baseURL = 'http://127.0.0.1:8000') {
    this.baseURL = baseURL;
  }

  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = this.getAccessToken();

    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(url, config);

    if (response.status === 401) {
      // Попытка обновить токен
      const refreshed = await this.refreshToken();
      if (refreshed) {
        config.headers['Authorization'] = `Bearer ${this.getAccessToken()}`;
        return fetch(url, config);
      }
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.message || 'Request failed');
    }

    return response.json();
  }

  async register(username, email, password, role) {
    return this.request('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({
        username,
        email,
        password,
        confirm_password: password,
        role,
      }),
    });
  }

  async login(username, password) {
    const data = await this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  }

  async refreshToken() {
    const refresh = this.getRefreshToken();
    if (!refresh) return false;

    try {
      const data = await this.request('/auth/refresh/', {
        method: 'POST',
        body: JSON.stringify({ token: refresh }),
      });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      return true;
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return false;
    }
  }

  async logout() {
    const refresh = this.getRefreshToken();
    if (refresh) {
      await this.request('/auth/logout/', {
        method: 'POST',
        body: JSON.stringify({ token: refresh }),
      });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Вакансии
  async getVacancies(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/vacancies/${queryString ? '?' + queryString : ''}`);
  }

  async getVacancy(id) {
    return this.request(`/api/vacancies/${id}/`);
  }

  async createVacancy(vacancyData) {
    return this.request('/api/vacancies/', {
      method: 'POST',
      body: JSON.stringify(vacancyData),
    });
  }

  async updateVacancy(id, vacancyData) {
    return this.request(`/api/vacancies/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(vacancyData),
    });
  }

  async deleteVacancy(id) {
    return this.request(`/api/vacancies/${id}/`, {
      method: 'DELETE',
    });
  }

  // Резюме
  async getResumes(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/resumes/${queryString ? '?' + queryString : ''}`);
  }

  async createResume(resumeData) {
    return this.request('/api/resumes/', {
      method: 'POST',
      body: JSON.stringify(resumeData),
    });
  }

  // Отклики
  async applyToVacancy(vacancyId, coverLetter, resumeId = null) {
    return this.request(`/api/vacancies/${vacancyId}/apply/`, {
      method: 'POST',
      body: JSON.stringify({
        cover_letter: coverLetter,
        ...(resumeId && { resume_id: resumeId }),
      }),
    });
  }

  // Избранное
  async toggleFavorite(vacancyId) {
    return this.request(`/api/vacancies/${vacancyId}/favorite/`, {
      method: 'POST',
    });
  }
}

// Использование
const api = new JobSearchAPI();

// Регистрация
await api.register('seeker1', 'seeker@example.com', 'password123', 'seeker');

// Вход
await api.login('seeker1', 'password123');

// Получить вакансии
const vacancies = await api.getVacancies({ t: 'python' });

// Откликнуться на вакансию
await api.applyToVacancy(1, 'Я заинтересован в этой вакансии', 1);

// Добавить в избранное
await api.toggleFavorite(1);
```

---

## Коды статусов HTTP

- `200 OK` - успешный запрос
- `201 Created` - ресурс успешно создан
- `204 No Content` - успешное удаление
- `400 Bad Request` - неверный запрос
- `401 Unauthorized` - требуется аутентификация
- `403 Forbidden` - недостаточно прав
- `404 Not Found` - ресурс не найден
- `500 Internal Server Error` - ошибка сервера

---

## Типы данных

### Роли пользователей
- `seeker` - соискатель
- `employer` - работодатель

### Типы занятости (employment_type)
- `full_time` - Полная занятость
- `part_time` - Частичная занятость
- `contract` - Контракт
- `internship` - Стажировка
- `fifo` - FIFO / Вахта
- `volunteer` - Волонтерство

### Форматы работы (work_format)
- `on_site` - В офисе
- `remote` - Удаленно
- `hybrid` - Гибридный
- `shift` - Сменная работа

### Требуемый опыт (experience_required)
- `no_exp` - Без опыта
- `1_3` - 1–3 года
- `3_6` - 3–6 лет
- `6_plus` - 6+ лет

### Статусы отклика (status)
- `pending` - Ожидает рассмотрения
- `reviewed` - Рассмотрено
- `accepted` - Принято
- `rejected` - Отклонено

---

## Swagger документация

Интерактивная документация API доступна по адресу:
```
http://127.0.0.1:8000/docs/
```

В Swagger UI вы можете:
- Просмотреть все эндпоинты
- Увидеть схемы запросов/ответов
- Протестировать API прямо в браузере
- Авторизоваться через JWT токены (кнопка "Authorize")

---

## Обработка ошибок

Всегда проверяйте статус ответа перед обработкой данных:

```javascript
const response = await fetch('http://127.0.0.1:8000/api/vacancies/');

if (!response.ok) {
  const error = await response.json();
  console.error('Ошибка:', error);
  // Обработка ошибки
  return;
}

const data = await response.json();
// Обработка данных
```

---

## Примечания

1. **Access токен** действителен 15 минут. Реализуйте автоматическое обновление токена при получении 401 ошибки.

2. **Refresh токен** действителен 1 день. После выхода (logout) refresh токен добавляется в blacklist и больше не может быть использован.

3. **Повторные отклики** на одну вакансию невозможны - система автоматически предотвращает это.

4. **Счетчик просмотров** вакансий увеличивается автоматически при каждом GET запросе деталей вакансии.

5. **Избранное** работает как toggle - один и тот же эндпоинт добавляет или удаляет вакансию из избранного.

---

## Поддержка

При возникновении вопросов обращайтесь к бэкенд разработчику или проверьте Swagger документацию по адресу `/docs/`.

