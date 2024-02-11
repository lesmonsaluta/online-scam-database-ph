from tortoise import fields, models

class text_messages(models.Model):
    id = fields.IntField(pk=True)  
    sim_number = fields.CharField(max_length=1000, unique=False) 
    detected_text = fields.TextField(max_length=1000, unique=False) 
    image_file = fields.BinaryField(null=True)
    blob_hash = fields.CharField(max_length=64, null=False, unique=True) 
    
    class Meta:
        table = "text_messages"