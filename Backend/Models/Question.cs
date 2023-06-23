using System;

using System.ComponentModel.DataAnnotations;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class Question
{
    [Key]
    public string QuestionText { get; set; }
    public int QuestionID { get; set; }
    public string Difficulty { get; set; }
}

public class MyDbContext : DbContext
{
    public DbSet<Question> Maths { get; set; }

    public string retrieveQuestions()
    {
        using (var db = new MyDbContext())
        {
            var math = db.Maths.Select(q => new { q.QuestionID, q.QuestionText, q.Difficulty }).ToList();

            var tuples = math.Select(r => (r.QuestionID, r.QuestionText, r.Difficulty)).ToList();

            // Serialize the list of tuples to JSON
            var json_questions = JsonSerializer.Serialize(tuples);

            return json_questions;

        }

    }
}