using System;

using System.ComponentModel.DataAnnotations;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class Question
{
    public int Id { get; set; }
    public string QuestionText { get; set; }
    public string Answer { get; set; }
    public string Explanation { get; set; }
    public Difficulty Difficulty { get; set; }
}

public enum Difficulty
{
    Easy,
    Medium,
    Hard
}