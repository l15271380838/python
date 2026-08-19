from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware  # 新增
from app.config import settings
from app.routers import demo, conversation, chat
from contextlib import asynccontextmanager


app = FastAPI(
    title="ai",
    description="学习",
    version="0.1.0",
    debug=settings.debug,
)


# 跨域配置，对应 NestJS 的 app.enableCors()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境改成具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行（对应 NestJS 的 onModuleInit）
    print("✅ 应用启动，初始化资源...")
    # 后面章节在这里初始化数据库连接池、LangChain 模型等
    yield
    # 应用关闭时执行（对应 NestJS 的 onModuleDestroy）
    print("👋 应用关闭，清理资源...")


# 全局异常处理：请求参数验证失败
# 对应 NestJS 的 ValidationPipe + ExceptionFilter
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": " -> ".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=422,
        content={"code": 422, "message": "请求参数验证失败", "errors": errors},
    )

    # 全局异常处理：业务异常（HTTPException）


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "服务器内部错误", "detail": str(exc)},
    )


app.include_router(demo.router)
app.include_router(conversation.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"mes": "启动成功", "model": settings.model_name}


@app.get("/health")
async def health_check():
    return {"type": "ok"}
