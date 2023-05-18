protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative myauth/myauth.proto 
python -m grpc_tools.protoc -I./myauth --python_out=./myauth/ --pyi_out=./myauth/ --grpc_python_out=./myauth/ myauth/myauth.proto
