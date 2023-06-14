using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class Question {
    public int Id { get; set;}
    public string Query { get; set;}
    public HashSet<AnswerOption> Options { get; set; }
    public int Answer { get; set; }
}