using Backend.Data;
using Microsoft.EntityFrameworkCore;
using Backend.Models;

namespace Backend.Models;

public class DatabaseContext : DbContext
{
    public DatabaseContext(DbContextOptions<DatabaseContext> options)
        : base(options)
    {
        DbInitialiser.Initialise(this);

    }
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer("Server=tcp:its-sql-db-server.database.windows.net,1433;Initial Catalog=ITS;Persist Security Info=False;User ID=itsadmin;Password=IT$project;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;");
    }

    public DbSet<Backend.Models.User> Users { get; set; }  = default!;

    public DbSet<Backend.Models.Course> Course { get; set; } = default!;

    public DbSet<Backend.Models.Question> Question { get; set; } = default!;

    public DbSet<Backend.Models.AnswerOption> Answer { get; set; } = default!;

    public DbSet<Backend.Models.Test> Test { get; set; } = default!;
}