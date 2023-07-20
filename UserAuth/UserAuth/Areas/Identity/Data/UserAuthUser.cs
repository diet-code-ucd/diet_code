using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace UserAuth.Areas.Identity.Data;

// Add profile data for application users by adding properties to the UserAuthUser class
public class UserAuthUser : IdentityUser
{
    [PersonalData]
    [Column(TypeName ="nvarchar(100)")]
    public string FirstName { get; set; }

    [PersonalData]
    [Column(TypeName = "nvarchar(100)")]
    public string LastName { get; set; }

    [PersonalData]
    [Column(TypeName = "nvarchar(100)")]
    public string UserGoal { get; set; }

    [PersonalData]
    [Column(TypeName = "date")]
    public DateTime DateOfBirth { get; set; }
}

