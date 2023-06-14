using System.ComponentModel.DataAnnotations;

namespace Backend.Models;

public class Question {
    public int Id { get; set;}
    public string? question { get; set; }
    public string? optionA { get; set; }
    public string? optionB { get; set; }
    public string? optionC { get; set; }
    public string? optionD { get; set; }
    public string? answer { get; set; }
}