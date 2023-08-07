from django.db import models
from ..accounts.models import Region, Department, STATES_STATUSES, User
from django.utils.timezone import now
from ..core.models import TimestampedModel


class TreeTypes(models.Model):
    name = models.CharField(max_length=120)
    show_profit = models.BooleanField(default=False)
    sort = models.IntegerField(blank=True, null=True, verbose_name='SORT NUMBER')
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    class Meta:
        db_table = "tree_types"
        verbose_name_plural = "TreeTypes"

    def __str__(self):
        return f"{self.name}"


class TreeCategory(TimestampedModel):
    name = models.CharField(max_length=64)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    class Meta:
        db_table = "tree_category"
        verbose_name_plural = "TreeCategory"

    def __str__(self):
        return f"{self.name}"


class TreePlant(TimestampedModel):
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    types = models.ManyToManyField(TreeTypes, verbose_name="Tree types", related_name="tree_types", blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)
    sort = models.IntegerField(blank=True, null=True, verbose_name='SORT NUMBER')
    is_show_sprouting = models.BooleanField(default=False)  # niholchilik
    is_show_seed = models.BooleanField(default=False)  # urug'chilik
    is_show_sapling = models.BooleanField(default=False)  # ko'chatchilik
    is_show_height = models.BooleanField(default=False)  # ko'chat balanligi

    class Meta:
        ordering = ('sort',)
        db_table = "tree_plant"
        verbose_name_plural = "TreePlant"

    def __str__(self):
        return f"{self.name}"

    def _types(self):
        data = ".".join(item.name for item in self.types.all())
        return data


class TreeHeightReport(TimestampedModel):
    tree_plan = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    height_0_0_2_count = models.FloatField(verbose_name="0,2 м гача", null=True, blank=True)
    height_0_2_5_count = models.FloatField(verbose_name="0,2 дан 0,5 м гача", null=True, blank=True)
    height_0_5_1_count = models.FloatField(verbose_name="0,5 -1 м. гача", null=True, blank=True)
    height_1_1_5_count = models.FloatField(verbose_name="1-1,5 м гача", null=True, blank=True)
    height_1_5_2_count = models.FloatField(verbose_name="1,5-2 м гача", null=True, blank=True)
    height_2_count = models.FloatField(verbose_name="2 м дан", null=True, blank=True)
    date = models.DateTimeField(default=now)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    class Meta:
        db_table = "tree_height"
        verbose_name_plural = "TreeHeightReport"

    def __str__(self):
        return f"Tree: {self.tree_plan} | Region:  {self.region.name}"


# ================KO'CHAT -> Sapling===================
class Sapling(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="growing_plant")
    count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="growing_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="growing_region")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="growing_creator", blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sapling"
        verbose_name_plural = "Sapling"


# ===============SaplingPlan -> ko'chatPlan============
class SaplingPlan(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="sapling_plan", blank=True, null=True)
    count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="growing_plan_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="growing_plan_region")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="growing_plan_creator", blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sapling_plan"
        verbose_name_plural = "SaplingPlan"


# ================SEED -> URUG=========================
class Seed(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="seed_plant")
    count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="seed_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="seed_region")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seed_creator", blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "seed"
        verbose_name_plural = "Seed"


# ================SEEDPlan -> UrugPlan=================
class SeedPlan(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="seed_plan_plant")
    count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="seed_plan_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="seed_plan_region")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seed_plan_creator", blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "seed_plan"
        verbose_name_plural = "SeedPlan"


# =================SproutActual -> Nihol=====================
class Sprout(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="sprout_plant")
    count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sprout_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="sprout_region")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sprout_creator", blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sprout"
        verbose_name_plural = "Sprout"


# =================SproutPlan -> NiholPlan============
class SproutPlan(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="sprout_plan_plant")
    count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sprout_plan_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="sprout_plan_region")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sprout_plan_creator", blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sprout_plan"
        verbose_name_plural = "SproutPlan"


# =================Kochat kirim -> SaplingInput=====
class SaplingInput(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)
    donation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Beg'araz olindi
    buying = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Sotib olingan
    new_sprout = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Yangi unib chiqdi
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sapling_input"
        verbose_name_plural = "SaplingInput"


# =================Kochat Chiqim -> SaplingOutput=====
class SaplingOutput(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)  #
    for_the_forest = models.DecimalField(max_digits=18, decimal_places=2, blank=True,
                                         null=True)  # Ўрмон барпо қилиш учун
    donation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Beg'araz berildi
    selling = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Sotib yuborildi
    unsuccessful = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Хатосига экилди
    place_changed = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Кўчириб экилди
    out_of_count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Ҳисобдан чиқарилган

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sapling_output"
        verbose_name_plural = "SaplingOutput"


# =================Urug' kirim -> SeedInput=====
class SeedInput(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)  #
    donation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Beg'araz olindi
    buying = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Sotib olingan
    new_sprout = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Yangi unib chiqdi
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "seed_input"
        verbose_name_plural = "SeedInput"


# =================Urug' chiqim -> SeedOutput=====
class SeedOutput(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)  #
    for_the_forest = models.DecimalField(max_digits=18, decimal_places=2, blank=True,
                                         null=True)  # Ўрмон ва плантация барпо қилиш учун
    donation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Beg'araz berildi
    selling = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Sotib yuborildi
    unsuccessful = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Хатосига экилди
    place_changed = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Кўчириб экилди
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "seed_output"
        verbose_name_plural = "SeedOutput"


# =================Nihol kirim -> SproutInput=====
class SproutInput(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)  #
    donation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Beg'araz olindi
    buying = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Sotib olingan
    new_sprout = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Yangi unib chiqdi
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sprout_input"
        verbose_name_plural = "SproutInput"


# =================Nihol chiqim -> SproutOutput=====
class SproutOutput(TimestampedModel):
    date = models.DateTimeField()
    plant = models.ForeignKey(TreePlant, on_delete=models.CASCADE)
    category = models.ForeignKey(TreeCategory, on_delete=models.CASCADE, blank=True, null=True)
    for_the_forest = models.DecimalField(max_digits=18, decimal_places=2, blank=True,
                                         null=True)  # Ўрмон ва плантация барпо қилиш учун
    donation = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Beg'araz berildi
    selling = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Sotib yuborildi
    unsuccessful = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Хатосига экилди
    place_changed = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Кўчириб экилди
    out_of_count = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Ҳисобдан чиқарилган
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "sprout_output"
        verbose_name_plural = "SproutOutput"


# URUG SEPISH SEED
class LandCategory(TimestampedModel):
    name = models.CharField(max_length=64)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    class Meta:
        db_table = "land_category"
        verbose_name_plural = "LandCategory"

    def __str__(self):
        return f"{self.name}"


class PrepairLand(TimestampedModel):
    date = models.DateTimeField()
    hectare = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    categories = models.ForeignKey(LandCategory, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "prepair_land"
        verbose_name_plural = "PrepairLand"


class PrepairLandPlan(TimestampedModel):
    date = models.DateTimeField()
    hectare = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    categories = models.ForeignKey(LandCategory, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "prepair_land_plan"
        verbose_name_plural = "PrepairLandPlan"


# MAXSUS DARAXTLAR EKISH DARAXT EKISH

class TreeGroundPlanting(TimestampedModel):
    date = models.DateTimeField()
    desert_plant = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # cho'l o'simligi
    walnut = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # grek yongoq
    pistachios = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # pista
    nut = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # bodom
    poplar = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # terak
    paulownia = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Pavlovniya
    other_plants = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # boshqa daraxtlar
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "tree_ground_planting"
        verbose_name_plural = "TreePlanting"


class TreeGroundPlantingPlan(TimestampedModel):
    date = models.DateTimeField()
    desert_plant = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # cho'l o'simligi
    walnut = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # grek yongoq
    pistachios = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # pista
    nut = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # bodom
    poplar = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # terak
    paulownia = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # Pavlovniya
    other_plants = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # boshqa daraxtlar
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "tree_ground_planting_plan"
        verbose_name_plural = "TreeGroundPlantingPlan"


class TreeContractCategory(TimestampedModel):
    name = models.CharField(max_length=400, blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tree_contract_category'
        verbose_name_plural = "TreeContractCategory"


class TreeContract(TimestampedModel):
    category = models.ForeignKey(TreeContractCategory, on_delete=models.CASCADE)
    count = models.FloatField(blank=True, null=True)  # MING DONA
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # MLN SO"M
    payout = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # TO"LANGAM MABLAG"
    output_tree = models.FloatField(blank=True, null=True)  # OLIB KETILGAN KO"CHAT
    date = models.DateTimeField(default=now)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    class Meta:
        db_table = "tree_contract"
        verbose_name_plural = "TreeContract"

    def __int__(self):
        return self.id


class TreeContractPlan(TimestampedModel):
    tree_count = models.FloatField(blank=True, null=True)  # MING DONA
    date = models.DateTimeField(default=now)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    class Meta:
        db_table = "tree_contract_plan"
        verbose_name_plural = "TreeContractPlan"

    def __int__(self):
        return self.id