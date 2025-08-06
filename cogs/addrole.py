import discord
from discord.ext import commands

class AddRoleButtonView(discord.ui.View):
    def __init__(self, role: discord.Role):
        super().__init__(timeout=None)
        self.role = role

    @discord.ui.button(label="獲得角色", style=discord.ButtonStyle.primary, custom_id="add_role_button_persistent")
    async def add_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.role in interaction.user.roles:
            await interaction.response.send_message(f"you already have {self.role.name} role", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(f"you get {self.role.name} role", ephemeral=True)

class AddRoleButtonCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="addrolebutton")
    async def add_role_button(self, ctx, role: discord.Role, *, message: str = None):
        
        view = AddRoleButtonView(role)
        channel = self.bot.get_channel(1401588928351572018)
        if not message:
            message = f"點擊下方按鈕即可獲得 {role.mention} 角色！"
        await channel.send(message, view=view)
        
    async def cog_load(self):
        self.bot.add_view(AddRoleButtonView(None))

async def setup(bot: commands.Bot):
    await bot.add_cog(AddRoleButtonCog(bot))
    print("AddRoleButtonCog has been loaded.")