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

            //This is to eliminate conversion of some signs to unicode ex: '+' was converted to \u002
            var serializeOptions = new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            };


            // Serialize the list JSON
            var json_questions = JsonSerializer.Serialize(math,serializeOptions);

            return json_questions;

        }

    }
}