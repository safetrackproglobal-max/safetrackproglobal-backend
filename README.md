### Step 1: Set Up Your Project

1. **Initialize a new Node.js project**:
   ```bash
   mkdir safetrack-pro-backend
   cd safetrack-pro-backend
   npm init -y
   ```

2. **Install required packages**:
   ```bash
   npm install express mongoose multer cors dotenv
   ```

   - **express**: Web framework for Node.js.
   - **mongoose**: MongoDB object modeling tool.
   - **multer**: Middleware for handling `multipart/form-data`, used for uploading files.
   - **cors**: Middleware to enable Cross-Origin Resource Sharing.
   - **dotenv**: Module to load environment variables from a `.env` file.

### Step 2: Create the Project Structure

Create the following folder structure:

```
safetrack-pro-backend/
│
├── models/
│   ├── RiskAssessment.js
│   └── User.js
│
├── routes/
│   ├── api.js
│
├── .env
├── server.js
└── package.json
```

### Step 3: Create the Models

**1. User Model (`models/User.js`)**:
```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    email: { type: String, required: true, unique: true },
});

module.exports = mongoose.model('User', userSchema);
```

**2. Risk Assessment Model (`models/RiskAssessment.js`)**:
```javascript
const mongoose = require('mongoose');

const riskAssessmentSchema = new mongoose.Schema({
    projectId: { type: mongoose.Schema.Types.ObjectId, ref: 'Project' },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    imageUrl: String,
    chemicals: [{
        name: String,
        formula: String,
        concentration: String,
        hazards: [String]
    }],
    hazards: [{
        type: String,
        severity: Number,
        location: { x: Number, y: Number },
        recommendedActions: [String]
    }],
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('RiskAssessment', riskAssessmentSchema);
```

### Step 4: Create the Routes

**API Routes (`routes/api.js`)**:
```javascript
const express = require('express');
const multer = require('multer');
const RiskAssessment = require('../models/RiskAssessment');
const User = require('../models/User');

const router = express.Router();
const upload = multer({ dest: 'uploads/' }); // Directory for uploaded files

// User registration
router.post('/register', async (req, res) => {
    const { username, password, email } = req.body;
    const user = new User({ username, password, email });
    try {
        await user.save();
        res.status(201).json({ message: 'User registered successfully' });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Image analysis endpoint
router.post('/analyze-image', upload.single('image'), async (req, res) => {
    try {
        const imageUrl = req.file.path; // Path to the uploaded image
        // Call your AI service here for analysis
        const analysisResults = {}; // Replace with actual analysis results

        // Save the risk assessment
        const assessment = new RiskAssessment({
            imageUrl,
            // Add other fields as necessary
        });
        await assessment.save();

        res.json({ success: true, data: assessment });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get all risk assessments
router.get('/assessments', async (req, res) => {
    try {
        const assessments = await RiskAssessment.find();
        res.json(assessments);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
```

### Step 5: Set Up the Server

**Server Configuration (`server.js`)**:
```javascript
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const apiRoutes = require('./routes/api');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use('/api', apiRoutes);

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```

### Step 6: Create the `.env` File

Create a `.env` file in the root of your project and add your MongoDB connection string:

```
MONGODB_URI=mongodb://<username>:<password>@localhost:27017/safetrackpro
```

### Step 7: Run the Server

1. **Start the server**:
   ```bash
   node server.js
   ```

2. **Test the API**: You can use tools like Postman or Insomnia to test your API endpoints.

### Conclusion

You now have a basic backend for the SafeTrack Pro web application using Node.js and Express. You can expand this by adding authentication, more complex image analysis, and additional endpoints as needed.