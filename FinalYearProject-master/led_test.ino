void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);   
}
void loop() {
  digitalWrite(13, HIGH);   
  Serial.println("high");
  delay(2000);              
  digitalWrite(13, LOW);
  Serial.println("low");   
  delay(2000);             
}
