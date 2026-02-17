const express = require('express');
const router = express.Router();
const User = require('../models/user');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');


// Register a new user
router.post('/register', async (req,res) =>{
     try {
        const {name , email,password, date} = req.body;

        // Check if user already exists
        let user = await User.findOne({ email });
        if(user){
            return res.status(400).json({ message: "User already exists" });

     }

    //  create new user object
    user = new User({
        name,
        email,
        password,
        date
    });

    // Hash the password
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(password, salt);
    
    await user.save();
    res.status(201).json({ message: "User registered successfully! 🎉" });
} catch(err) {
    console.error("Registration Error: ", err.message);
    res.status(500).json({ message: "Server Error during registration" });
}});

// Login user
router.post('/login', async (req,res) => {
    try {
        const {email, password} = req.body;

        // Check if user exists
        const user = await User.findOne({ email });
        if(!user){
            return res.status(400).json({ message: "INVALID CREDENTIALS" });
        }

        
       // Compare password
        const isMatch = await bcrypt.compare(password, user.password);
        console.log("SPY LOG - Did passwords match?: ", isMatch); // ADD THIS LINE

        if(!isMatch){
            console.log("SPY LOG - Kicked out by the Bouncer!"); // ADD THIS LINE
            return res.status(400).json({ message: "INVALID CREDENTIALS" });
        }

        // Create JWT Payload
        const payload = {
            user : {
                id: user.id,
                name: user.name,
                email: user.email
            }
        }

        // Sign Token
       // Sign the token using our secret vault key
        jwt.sign(
            payload,
            process.env.JWT_SECRET,
            { expiresIn: '7d' }, // The token will expire in 7 days for security
            (err, token) => {
                if (err) throw err;
                res.json({ 
                    message: "Login successful! 🚀",
                    token: token 
                });
            }
        );
    } catch(err) {
        console.error("Login Error: ", err.message);
        res.status(500).json({ message: "Server Error during login" });
    }
});
module.exports = router;