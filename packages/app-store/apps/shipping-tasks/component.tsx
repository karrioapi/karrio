import React, { useState, useEffect } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Plus, CheckCircle, Circle, Trash2, Package, Clock, AlertCircle } from "lucide-react";
import type { AppComponentProps } from "../../types";

interface Task {
    id: string;
    title: string;
    description?: string;
    priority: "low" | "medium" | "high" | "urgent";
    category: string;
    completed: boolean;
    created_at: string;
    completed_at?: string;
}

export default function ShippingTasksComponent({ app, context }: AppComponentProps) {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newTaskTitle, setNewTaskTitle] = useState("");
    const [newTaskCategory, setNewTaskCategory] = useState("");
    const [newTaskPriority, setNewTaskPriority] = useState<Task["priority"]>("medium");
    const [filter, setFilter] = useState<"all" | "pending" | "completed">("all");

    // Get configuration from app installation metafields
    const config = app.installation?.metafields?.reduce((acc, field) => {
        acc[field.key] = field.value;
        return acc;
    }, {} as Record<string, any>) || {};

    const defaultPriority = config.default_priority || "medium";
    const taskCategories = config.task_categories
        ? config.task_categories.split(",").map((cat: string) => cat.trim())
        : ["Pickup", "Delivery", "Documentation", "Customer Service"];
    const workspaceName = config.workspace_name || context.workspace?.name || "Shipping Workspace";
    const dailyTaskLimit = parseInt(config.daily_task_limit) || 10;

    // Load tasks from localStorage on component mount
    useEffect(() => {
        const savedTasks = localStorage.getItem(`shipping-tasks-${context.workspace?.id}`);
        if (savedTasks) {
            setTasks(JSON.parse(savedTasks));
        }
    }, [context.workspace?.id]);

    // Save tasks to localStorage whenever tasks change
    useEffect(() => {
        localStorage.setItem(`shipping-tasks-${context.workspace?.id}`, JSON.stringify(tasks));
    }, [tasks, context.workspace?.id]);

    const addTask = () => {
        if (!newTaskTitle.trim()) return;

        const newTask: Task = {
            id: Date.now().toString(),
            title: newTaskTitle.trim(),
            priority: newTaskPriority,
            category: newTaskCategory || taskCategories[0],
            completed: false,
            created_at: new Date().toISOString(),
        };

        setTasks(prev => [newTask, ...prev]);
        setNewTaskTitle("");
        setNewTaskCategory("");
        setNewTaskPriority(defaultPriority as Task["priority"]);
    };

    const toggleTask = (taskId: string) => {
        setTasks(prev => prev.map(task =>
            task.id === taskId
                ? {
                    ...task,
                    completed: !task.completed,
                    completed_at: !task.completed ? new Date().toISOString() : undefined
                }
                : task
        ));
    };

    const deleteTask = (taskId: string) => {
        setTasks(prev => prev.filter(task => task.id !== taskId));
    };

    const getPriorityColor = (priority: Task["priority"]) => {
        switch (priority) {
            case "urgent": return "bg-red-100 text-red-800 border-red-200";
            case "high": return "bg-orange-100 text-orange-800 border-orange-200";
            case "medium": return "bg-blue-100 text-blue-800 border-blue-200";
            case "low": return "bg-gray-100 text-gray-800 border-gray-200";
            default: return "bg-gray-100 text-gray-800 border-gray-200";
        }
    };

    const getPriorityIcon = (priority: Task["priority"]) => {
        switch (priority) {
            case "urgent": return <AlertCircle className="h-3 w-3" />;
            case "high": return <Clock className="h-3 w-3" />;
            default: return null;
        }
    };

    const filteredTasks = tasks.filter(task => {
        if (filter === "pending") return !task.completed;
        if (filter === "completed") return task.completed;
        return true;
    });

    const pendingTasks = tasks.filter(task => !task.completed);
    const completedTasks = tasks.filter(task => task.completed);

    return (
        <div className="p-6 max-w-4xl mx-auto space-y-6">
            {/* Welcome Header */}
            <Card>
                <CardHeader>
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <Package className="h-6 w-6 text-blue-600" />
                        </div>
                        <div>
                            <CardTitle className="text-xl">Welcome to Shipping Tasks</CardTitle>
                            <CardDescription>
                                Manage your shipping workflow with {workspaceName}
                            </CardDescription>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="text-center p-4 bg-blue-50 rounded-lg">
                            <div className="text-2xl font-bold text-blue-600">{pendingTasks.length}</div>
                            <div className="text-sm text-blue-700">Pending Tasks</div>
                        </div>
                        <div className="text-center p-4 bg-green-50 rounded-lg">
                            <div className="text-2xl font-bold text-green-600">{completedTasks.length}</div>
                            <div className="text-sm text-green-700">Completed Today</div>
                        </div>
                        <div className="text-center p-4 bg-purple-50 rounded-lg">
                            <div className="text-2xl font-bold text-purple-600">{taskCategories.length}</div>
                            <div className="text-sm text-purple-700">Categories</div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Add New Task */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-lg">Add New Task</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col sm:flex-row gap-3">
                        <Input
                            placeholder="Enter task title..."
                            value={newTaskTitle}
                            onChange={(e) => setNewTaskTitle(e.target.value)}
                            onKeyPress={(e) => e.key === "Enter" && addTask()}
                            className="flex-1"
                        />
                        <Select value={newTaskCategory} onValueChange={setNewTaskCategory}>
                            <SelectTrigger className="w-full sm:w-48">
                                <SelectValue placeholder="Category" />
                            </SelectTrigger>
                            <SelectContent>
                                {taskCategories.map(category => (
                                    <SelectItem key={category} value={category}>
                                        {category}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Select value={newTaskPriority} onValueChange={(value) => setNewTaskPriority(value as Task["priority"])}>
                            <SelectTrigger className="w-full sm:w-32">
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="low">Low</SelectItem>
                                <SelectItem value="medium">Medium</SelectItem>
                                <SelectItem value="high">High</SelectItem>
                                <SelectItem value="urgent">Urgent</SelectItem>
                            </SelectContent>
                        </Select>
                        <Button onClick={addTask} disabled={!newTaskTitle.trim()}>
                            <Plus className="h-4 w-4 mr-1" />
                            Add
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Task Filters */}
            <div className="flex items-center justify-between">
                <div className="flex gap-2">
                    <Button
                        variant={filter === "all" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFilter("all")}
                    >
                        All ({tasks.length})
                    </Button>
                    <Button
                        variant={filter === "pending" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFilter("pending")}
                    >
                        Pending ({pendingTasks.length})
                    </Button>
                    <Button
                        variant={filter === "completed" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFilter("completed")}
                    >
                        Completed ({completedTasks.length})
                    </Button>
                </div>
            </div>

            {/* Task List */}
            <div className="space-y-3">
                {filteredTasks.length === 0 ? (
                    <Card>
                        <CardContent className="py-8 text-center text-gray-500">
                            {filter === "all" && "No tasks yet. Add your first shipping task above!"}
                            {filter === "pending" && "No pending tasks. Great job!"}
                            {filter === "completed" && "No completed tasks yet."}
                        </CardContent>
                    </Card>
                ) : (
                    filteredTasks.slice(0, dailyTaskLimit).map(task => (
                        <Card key={task.id} className={`transition-all ${task.completed ? "opacity-75" : ""}`}>
                            <CardContent className="py-4">
                                <div className="flex items-center gap-3">
                                    <Checkbox
                                        checked={task.completed}
                                        onCheckedChange={() => toggleTask(task.id)}
                                        className="mt-1"
                                    />
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2 mb-1">
                                            <h3 className={`font-medium ${task.completed ? "line-through text-gray-500" : ""}`}>
                                                {task.title}
                                            </h3>
                                            <Badge variant="outline" className={`text-xs ${getPriorityColor(task.priority)}`}>
                                                {getPriorityIcon(task.priority)}
                                                <span className="ml-1">{task.priority}</span>
                                            </Badge>
                                        </div>
                                        <div className="flex items-center gap-2 text-sm text-gray-500">
                                            <Badge variant="secondary" className="text-xs">
                                                {task.category}
                                            </Badge>
                                            <span>•</span>
                                            <span>
                                                {task.completed
                                                    ? `Completed ${new Date(task.completed_at!).toLocaleDateString()}`
                                                    : `Created ${new Date(task.created_at).toLocaleDateString()}`
                                                }
                                            </span>
                                        </div>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => deleteTask(task.id)}
                                        className="text-gray-400 hover:text-red-500"
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}

                {filteredTasks.length > dailyTaskLimit && (
                    <Card>
                        <CardContent className="py-4 text-center text-gray-500">
                            Showing {dailyTaskLimit} of {filteredTasks.length} tasks.
                            <br />
                            <span className="text-xs">Adjust the daily limit in app settings to see more.</span>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
}
