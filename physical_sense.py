from pydantic import BaseModel, Field
import json, random, time

class PhysicalEvent(BaseModel):
    sensor_id: str = Field("thermo-01", description="传感器唯一ID")
    timestamp: float = Field(default_factory=time.time)
    temperature: float = Field(ge=-50.0, le=150.0, description="温度 (℃)")
    humidity: float = Field(ge=0.0, le=100.0, description="湿度 (%)")
    power_draw: float = Field(ge=0.0, description="瞬时功耗 (W)")

while True:
    event = PhysicalEvent(
        temperature=round(random.uniform(20.0, 35.0), 2),
        humidity=round(random.uniform(40.0, 80.0), 2),
        power_draw=round(random.uniform(5.0, 120.0), 1)
    )
    print(event.model_dump_json())
    time.sleep(2)