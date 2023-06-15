using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class DatabaseContext : DbContext
{
    public DatabaseContext(DbContextOptions<DatabaseContext> options)
        : base(options)
    {
    }   

    public DbSet<Course> Courses { get; set; } = null!;
    public DbSet<Question> Questions { get; set; } = null!;
    public DbSet<AnswerOption> AnswerOptions { get; set; } = null!;
}