const  express = require('express');
const router = express.Router();
const Expense = require('../models/expenses');
const auth = require('../MIDDLEWARES/authMiddlewares.js');

// Create a new expense
router.post('/add', auth, async (req, res) => {
    try {
        const { title, amount , category, platform, date, userId } = req.body;

        const newExpense = new Expense({
            title,
            amount,
            category,
            platform,
            date,
            user: req.user.id, // Use the user ID from the authenticated request
        });
    const savedExpense = await newExpense.save();
    res.status(201).json(savedExpense);
    } catch (error) {
        console.error("Error adding expense: ", error);
        res.status(500).json({ message: "Server error while adding expense" });
    }});

    // @route   GET api/expenses
// @desc    Get all expenses for a specific user
router.get('/', auth, async (req, res) => {
    try {
        // Find expenses where the 'user' field matches the logged-in user's ID
        const expenses = await Expense.find({ user: req.user.id }).sort({ date: -1 });
        res.json(expenses);
    } catch (err) {
        res.status(500).send('Server Error');
    }
});


// 1. Create a PUT route that takes the expense ID in the URL (e.g., /:id)
// 2. Add the 'auth' middleware (only logged-in users can edit)
// 3. START TRY/CATCH
//    A. Pull the updated data (title, amount, category) from req.body.
//    B. Find the expense by the ID from the URL.
//    C. IF it doesn't exist: Return 404 (Not Found).
//    D. SECURITY CHECK: Compare expense.user.toString() with req.user.id.
//       (If they don't match, return 401 - Not Authorized).
//    E. If authorized: Use Expense.findByIdAndUpdate() to save the new data.
//       (Hint: Use the { new: true } option so it returns the updated document).
//    F. Return the updated expense as JSON.
// 4. END TRY/CATCH (Handle server error).

router.put('/:id',auth, async(req, res)=>{
    try{
        const {title, amount, category} = req.body;
        let expense = await Expense.findById(req.params.id);
        if(!expense){
            return res.status(400).json({message: "Expense not found"});
        }
        //  D. SECURITY CHECK: Compare expense.user.toString() with req.user.id.
        //       (If they don't match, return 401 - Not Authorized).
        if(expense.user.toString() !== req.user.id){
            return res.status(401).json({message: "Unauthorized to update this expense"});
        }
        //    E. If authorized: Use Expense.findByIdAndUpdate() to save the new data.

        expense = await Expense.findByIdAndUpdate(
            req.params.id,
            { $set: { title, amount, category } },
            { new: true }
        )   
    
        //       (Hint: Use the { new: true } option so it returns the updated document).
        res.json(expense);
    } catch(error){
        res.status(500).json({message: "Server error while updating expense"});
    }
});

// 1. Create a DELETE route that takes the ID in the URL (/:id)
// 2. Add the 'auth' middleware.
// 3. START TRY/CATCH
//    A. Find the expense by the ID from the URL.
//    B. IF not found: Return 404 status.
//    C. SECURITY CHECK: Compare expense.user.toString() to req.user.id.
//       (If they don't match, return 401 - Not Authorized).
//    D. If authorized: Use await expense.deleteOne();
//    E. Return a success message: { message: "Expense deleted successfully" }
// 4. END TRY/CATCH

router.delete('/:id', auth, async (req,res)=>{
  try {
    const expense = await Expense.findById(req.params.id);
    if(!expense){
        return res.status(404).json({message: "Expense not found"});
    }
// securitty check
  if(expense.user.toString() !== req.user.id){
    return res.status(401).json({message: "Unauthorized to delete this expense"});
    }
    await expense.deleteOne();
    res.json({message: "Expense deleted successfully"});
  } 
  
  catch (error) {
    console.error("Delete Error:", error);
    res.status(500).json({ message: "Server error while deleting expense" });
  }
}
)
module.exports = router;